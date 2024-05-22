import socket
import json
import numpy as np
import argparse
import sys
import sklearn
import pandas as pd
import scipy
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
                                                        required=True, help='local computer server ip')
    parser.add_argument('--port', action="store", dest="port", type=int,
                                                        required=True, help='port you want to connect to')
    parser.add_argument('--evaluator_file', action="store", dest="evaluator_file",
                                                        required=True, help='path to evaluator .json file')


    given_args = parser.parse_args()
    host = given_args.host
    port = given_args.port
    evaluator_file = given_args.evaluator_file

    #try creating a socket
    try:
        # create a socket object
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print ("server_error: Error creating socket: %s" % e)
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
        print ("server_error: Connection error: %s" % e)
        sys.exit(1)

    while True:

        #send the evaluator json
        try:
            client.send(jsonResult.encode("utf-8")[:1024])
        except socket.error as e:
            print ("server_error: Error sending evaluator_file: %s" % e)
            sys.exit(1)


        # receive message from the server
        try:
            response = client.recv(1024)
            request = request.decode("utf-8") # convert bytes to string
            print(request)
            #save predictions
            with open('/Users/ishika/Desktop/API/Genomic-Model-Evaluation-API/examples/sampleRequest1/predictions.json', 'w', encoding='utf-8') as f:
                json.dump(request, f, ensure_ascii=False, indent=4)

        except socket.error as e:
            print ("server_error: Error receiving predictions: %s" % e)
            sys.exit(1)
        # if server sent us "closed" in the payload, we break out of the loop and close our socket
        if response.lower() == "closed":
            break

        print(response)

    # close client socket (connection to the server)
    client.close()
    print("Connection to server closed")

run_client()


## add code to be able to load predictions
mpra_sequences = pd.read_csv("/Users/ishika/Desktop/API/Genomic-Model-Evaluation-API/examples/sampleRequest1/mpra_evaluator_test_sequences.txt", header = None, sep=' ')
mpra_sequences.columns = ['seq_key', 'sequence', 'expression']

predictions_file = open('/Users/ishika/Desktop/API/Genomic-Model-Evaluation-API/examples/sampleRequest1/predictor_message_final.json')
predictions_file
predictions_file = json.load(predictions_file)
predictions = []
for i in predictions_file['predictions'][0]:
    predictions.append(predictions_file['predictions'][0][i])
measured = mpra_sequences['expression'].to_list()
### add some basic performance metric calculations
mse = sklearn.metrics.mean_squared_error(measured, predictions)
pearsonr = scipy.stats.pearsonr(measured, predictions)
f1_score = sklearn.metrics.f1_score(measured, predictions, average="weighted")
