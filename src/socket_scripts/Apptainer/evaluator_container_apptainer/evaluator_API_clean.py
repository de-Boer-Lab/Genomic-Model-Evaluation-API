#Oct 30th, 2024
import socket
import json
import numpy as np
import argparse
import sys
import os


def run_evaluator():
    parser = argparse.ArgumentParser(description='Socket Error Examples')
    parser.add_argument('--host', action="store", dest="host",required=True, help='predictor server ip address')
    parser.add_argument('--port', action="store", dest="port", type=int,required=True, help='predictor server port')
    parser.add_argument('--evaluator_file', action="store", dest="evaluator_file",required=True, help='path to evaluator .json file')

    given_args = parser.parse_args()
    host = given_args.host
    port = given_args.port
    evaluator_file = given_args.evaluator_file
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
    except socket.gaierror as e:
        print ("Address-related error connecting to server: %s" % e)
        sys.exit(1)
    except socket.error as e:
        print ("server_error: Connection error: %s" % e)
        sys.exit(1)

    try:
        #load in JSON file
        jsonResult = json.load(open(evaluator_file))
        jsonResult = json.dumps(jsonResult)
        print(jsonResult)
    except json.JSONDecodeError as e:
        print("Invalid JSON syntax:", e)

    #send the evaluator json to the predictor server

    try:
        print(len(jsonResult.encode("utf-8")))
        connection.sendall(jsonResult.encode("utf-8"))

        #sending this ends the stream to send
    except socket.error as e:
        print ("server_error: Error sending evaluator_file: %s" % e)
        sys.exit(1)
    # receive message from the server
    try:
        response = connection.recv(1024)
        response = response.decode("utf-8")
        response = json.loads(response) # convert bytes to string

        #save predictions to current working directory
        cwd = os.getcwd()
        with open(cwd + '/predictor_return_file.json', 'w', encoding='utf-8') as f:
            json.dump(response, f, ensure_ascii=False, indent=4)

    except socket.error as e:
        print ("server_error: Error receiving/saving predictions: %s" % e)
        sys.exit(1)

    connection.close()
    print("Connection to server closed")

run_evaluator()
