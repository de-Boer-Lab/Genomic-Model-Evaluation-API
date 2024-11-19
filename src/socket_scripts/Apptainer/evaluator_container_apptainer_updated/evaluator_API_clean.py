#Oct 30th, 2024
import socket
import json
import numpy as np
import argparse
import sys
import os
import struct


def run_evaluator():
    parser = argparse.ArgumentParser(description='Socket Error Examples')
    parser.add_argument('--host', action="store", dest="host",required=True, help='predictor server ip address')
    parser.add_argument('--port', action="store", dest="port", type=int,required=True, help='predictor server port')
    #parser.add_argument('--output_dir', action="store", dest="output_dir",required=True, help='output directory path to save predictions')

    given_args = parser.parse_args()
    host = given_args.host
    port = given_args.port
    #output_dir = given_args.output_dir
    #try creating a socket
    try:
        # create a socket object
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print ("server_error: Error creating socket: %s" % e)
        sys.exit(1)

    try:
        #establish connection with predictor server
        connection.connect((host, port))
        print(f"Connected to Predictor on {host}:{port}")
    except socket.gaierror as e:
        print ("Address-related error connecting to server: %s" % e)
        sys.exit(1)
    except socket.error as e:
        print ("server_error: Connection error: %s" % e)
        sys.exit(1)

    try:
        #load in JSON file from evalutor_data if Predictor container was successful
        jsonResult = json.load(open('/Users/ishika/Desktop/API/Genomic-Model-Evaluation-API/src/socket_scripts/Apptainer/evaluator_container_apptainer_updated/evaluator_data/evaluator_message_more_complex.json'))
        jsonResult = json.dumps(jsonResult)
        #print(jsonResult)
    except json.JSONDecodeError as e:
        print("Invalid JSON syntax:", e)

    #first send the total bytes we are transmitting to the Predictor
    #This is used to stop the recv() process
    #send the evaluator json to the predictor server
    try:
        # Length prefixing
        # Send Evaluator JSON length as a 4-byte integer
        jsonResult_bytes = jsonResult.encode("utf-8")
        jsonResults_total_bytes = len(jsonResult_bytes)

        connection.sendall(struct.pack('>I', jsonResults_total_bytes))
        print(f"Sent evaluator request length {jsonResults_total_bytes} bytes")

        connection.sendall(jsonResult_bytes)

    except socket.error as e:
        print ("server_error: Error sending evaluator_file: %s" % e)
        sys.exit(1)

# ---------------------- %%%%%%%---------------
    # receive message from the server
    json_data_recv = b''
    while True:
        # Before receiving JSON from Predictor
        # Receive length of the incoming JSON message (4-byte integer)
        # Can change to 8-byte integer by changing .recv(4) to .recv(8)
        # and replacing format string '>I' to '>Q'
        #Step 1
        try:
            msg_length = connection.recv(4)
            if not msg_length:
                print("Failed to receive message length. Closing connection.")
                connection.close()
                break # Exit the loop if no message length is received

            # Unpack meesage length from 4 bytes
            msglen = struct.unpack('>I', msg_length)[0]
            print(f"Expecting {msglen} bytes of data from the Predictor.")
            # Can comment out print commands other than for errors

            #Step 2
            # Now we want to receive the actual JSON in packets
            while len(json_data_recv) < msglen:
                packet = connection.recv(1024)
                if not packet:
                    print("Connection closed unexpectedly.")
                    break
                json_data_recv += packet
                #print(f"Received packet of {len(packet)} bytes, total received: {len(data)} bytes")

            # Decode and display the received data if all of it is received
            if len(json_data_recv) == msglen:
                print("Predictor return received compleatly")
                break
            else:
                print("Data received was incomplete or corrupted.")
                break


        except socket.error as e:
            print ("server_error: Error receiving predictions: %s" % e)
            sys.exit(1)

    predictor_response_full = json_data_recv
    predictor_json = predictor_response_full.decode("utf-8")
    predictor_json = json.loads(predictor_json)
    print(predictor_json)

#save predictions to current working directory

    cwd = os.getcwd()
    with open(cwd + '/predictions/predictor_return_file.json', 'w', encoding='utf-8') as f:
        json.dump(predictor_json, f, ensure_ascii=False, indent=4)

# ---------------------- %%%%%%%---------------

    connection.close()
    print("Connection to server closed")

run_evaluator()
