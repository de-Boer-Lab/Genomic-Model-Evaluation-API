import socket
import json
import numpy as np
import argparse
import sys
#read in JSON file here

evaluator_file = open('/Users/ishika/Desktop/API/Genomic-Model-Evaluation-API/examples/sampleRequest1/evaluator_message.json')

try:
    jsonResult = json.load(evaluator_file)
    print(jsonResult)
except json.JSONDecodeError as e:
    print("Invalid JSON syntax:", e)


def run_client():
    parser = argparse.ArgumentParser(description='Socket Error Examples')
    parser.add_argument('--host', action="store", dest="host",
                                                        required=False)
    parser.add_argument('--port', action="store", dest="port", type=int,
                                                        required=False)
    parser.add_argument('--file', action="store", dest="file",
                                                        required=False)

    given_args = parser.parse_args()
    host = given_args.host
    port = given_args.port
    evaluator_file = given_args.file

    #try creating a socket
    try:
        # create a socket object
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print ("Error creating socket: %s" % e)
        sys.exit(1)

    #try connecting to given host and port
    host = "127.0.0.1"  # replace with the server's IP address
    port = 8000  # replace with the server's port number


    try:
        #establish connection with server
        s.connect((host, port))
    except socket.gaierror as e:
        print ("Address-related error connecting to
                server: %s" % e)
        sys.exit(1)
    except socket.error as e:
        print ("Connection error: %s" % e)
        sys.exit(1)

    while True:

        #send the evaluator json
        try:
            client.send(jsonResult.encode("utf-8")[:1024])
        except socket.error as e:
            print ("Error sending evaluator_file: %s" % e)
            sys.exit(1)


        # receive message from the server
        try:
            response = client.recv(1024)
        except socket.error as e:
            print ("Error receiving predictions: %s" % e)
            sys.exit(1)
        # if server sent us "closed" in the payload, we break out of the loop and close our socket
        if response.lower() == "closed":
            break

        print(response)

    # close client socket (connection to the server)
    client.close()
    print("Connection to server closed")

run_client()
