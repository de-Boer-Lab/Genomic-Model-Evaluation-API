#Oct 30th, 2024
import socket
import json
import numpy as np
import argparse
import sys
import os
import struct

# Define constants
BYTESIZE = 100
ENCODER = "utf-8"


def run_evaluator():
    parser = argparse.ArgumentParser(description='Socket Error Examples')
    parser.add_argument('--host', action="store", dest="host",required=True, help='predictor server ip address')
    parser.add_argument('--port', action="store", dest="port", type=int,required=True, help='predictor server port')
    parser.add_argument('--evaluator_file', action="store", dest="evaluator_file",required=True, help='path to evaluator .json file')

    given_args = parser.parse_args()
    host = given_args.host
    port = given_args.port
    evaluator_file = given_args.evaluator_file

    # Load in JSON file
    # json.load() can cause memory issues for large files
    # with open() ensures Python closes the file as soon as reading operation is complete
    # frees up memory

    try:
        with open(evaluator_file, 'r') as file:
            jsonResult = json.load(file)
            jsonResult = json.dumps(jsonResult)  # Only needed if you need it as a JSON-formatted string
            print(jsonResult)
    except json.JSONDecodeError as e:
        print("Invalid JSON syntax:", e)
        exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        exit(1)

    # Convert the JSON data into bytes
    jsonResult_bytes = jsonResult.encode(ENCODER)
    jsonData_len = len(jsonResult_bytes)

    # Establish a socket connection
    try:
        # create a socket object
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Establish connection with predictor server
            connection.connect((host, port))
            print(f"Connected to Predictor on {host}:{port}")

            # Length prefixing
            # Send Evaluator JSON length as a 4-byte integer
            connection.sendall(struct.pack('>I', jsonData_len))
            print(f"Sent evaluator request length {jsonData_len} bytes")

            # Send Evaluator JSON in packets
            bytes_sent = 0
            while bytes_sent < jsonData_len:
                packet = jsonResult_bytes[bytes_sent:bytes_sent+BYTESIZE]
                connection.sendall(packet)
                bytes_sent += len(packet)

            print("Evaluator JSON sent successfully")

        except socket.gaierror as e:
            print ("Address-related error connecting to server: %s" % e)
            sys.exit(1)
    except socket.error as e:
        print ("server_error: Connection error: %s" % e)
        sys.exit(1)

    # # Send the JSON data in packets to the predictor server

    # try:
    #     print(len(jsonResult.encode(ENCODER)))
    #     connection.sendall(jsonResult.encode(ENCODER))

    #     #sending this ends the stream to send
    # except socket.error as e:
    #     print ("server_error: Error sending evaluator_file: %s" % e)
    #     sys.exit(1)

# ---------------------- %%%%%%%---------------
    # receive message from the server
    try:
        response = connection.recv(BYTESIZE)
        response = response.decode(ENCODER)
        response = json.loads(response) # convert bytes to string

        # save predictions to current working directory
        cwd = os.getcwd()
        with open(cwd + '/predictor_return_file.json', 'w', encoding=ENCODER) as f:
            json.dump(response, f, ensure_ascii=False, indent=4)

    except socket.error as e:
        print ("server_error: Error receiving/saving predictions: %s" % e)
        sys.exit(1)
# ---------------------- %%%%%%%---------------
    connection.close()
    print("Connection to server closed")

run_evaluator()
