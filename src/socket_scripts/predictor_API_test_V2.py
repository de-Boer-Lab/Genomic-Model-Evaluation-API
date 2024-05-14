import socket
import json
import numpy as np
import random
import base64
import sys
import os
from error_messages import *
from deBoerTest_model import *
# print(os.getcwd())
# os.chdir('/Users/ishika/Desktop/API/Genomic-Model-Evaluation-API/src/socket_scripts/')


def run_server():
    # create a socket object
    json_return_error = {}

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = '127.0.0.1'
    port = 8000

    # bind the socket to a specific address and port
    server.bind((server_ip, port))
    # listen for incoming connections
    server.listen(0)
    print(f"Listening on {server_ip}:{port}")

    # accept incoming connections
    client_socket, client_address = server.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

    # receive data from the client
    while True:
        request = client_socket.recv(1024)
        #gets the evaluator json file
        request = request.decode("utf-8") # convert bytes to string

        #check the evaluator_json
        #run error checking functions for bad prediction request

        try:
            data = json.loads(json_data)
            print(data)
        except json.JSONDecodeError as e:
            print("Invalid JSON syntax:", e)

        evaluator_file = open('/Users/ishika/Desktop/API/Genomic-Model-Evaluation-API/examples/sampleRequest1/evaluator_message.json')
        evaluator_json = json.load(evaluator_file)
        print(evaluator_json)


        check_mandatory_keys(evaluator_json.keys())
        check_task(evaluator_json['task'])
        check_prediction_types(evaluator_json['prediction_types'])
        check_cell_types_length(evaluator_json['prediction_types'], evaluator_json['cell_types'])
        check_scale_length(evaluator_json['prediction_types'], evaluator_json['scale'])
        check_prediction_ranges(evaluator_json['prediction_ranges'])
        check_seq_ids(evaluator_json['prediction_ranges'], evaluator_json['sequences'])
        check_key_values_readout(evaluator_json['readout'])
        check_key_values_strand(evaluator_json['strand'])
        check_key_values_scale(evaluator_json['scale'])
        check_key_values_flanks(evaluator_json['upstream_seq'], evaluator_json['downstream_seq'])
        #run the predictor container
        #check each sequence based on the model's specifications for
        #what characters and length is allowed for the sequence
        ##run error checking functions for prediction_request_failed

        print(request)

        #Send the sequences to the model
        #Return crap for each sequence regardless of what task is requested

        #information to return to evaluator
        json_return = {'task': evaluator_json['task'], 'prediction_types': evaluator_json['prediction_types']}
        json_return

        if evaluator_json['task'] == "help":
            help_file = "/Users/ishika/Desktop/API/Genomic-Model-Evaluation-API/examples/helpExample/predictor_message_onlyINFO_final.json"
            #send the evaluator json
            try:
                client_socket.send(help_file.encode("utf-8")[:1024])
            except socket.error as e:
                print ("Error sending help_file: %s" % e)
                sys.exit(1)
        sequences = evaluator_json['sequences']
        if evaluator_json['readout'] == "point":
            check_seqs_specifications(sequences)
            predictions_point = fake_model_point(sequences, json_return)

            json_string = json.dumps(predictions_point,
                                     ensure_ascii=False, indent=4)
            print(json_string)
            try:
                client_socket.send(json_string.encode("utf-8")[:1024])
            except socket.error as e:
                print ("Error sending predictor_file: %s" % e)
                sys.exit(1)

        if evaluator_json['readout'] == "track":
            check_seqs_specifications(sequences)
            predictions_track = fake_model_track(sequences, json_return)
            json_string = json.dumps(predictions_point,
                                     ensure_ascii=False, indent=4)
            try:
                client_socket.send(json_string.encode("utf-8")[:1024])
            except socket.error as e:
                print ("Error sending predictor_file: %s" % e)
                sys.exit(1)

        if evaluator_json['readout'] == "interaction_matrix":
            check_seqs_specifications(sequences)
            predictions_interaction_matrix = fake_model_interaction_matrix(sequences, json_return)
            json_string = json.dumps(predictions_point,
                                     ensure_ascii=False, indent=4)
            try:
                client_socket.send(json_string.encode("utf-8")[:1024])
            except socket.error as e:
                print ("Error sending predictor_file: %s" % e)
                sys.exit(1)

        #Format the json output file and send back to evaluator
        # if we receive "close" from the client, then we break
        # out of the loop and close the conneciton
        if request.lower() == "close":
            # send response to the client which acknowledges that the
            # connection should be closed and break out of the loop
            client_socket.send("closed".encode("utf-8"))
            break


        #jsonReceived = c.recv(1024)
        #print(jsonReceived)
        #print(f"Received: {request}")
        #response = "accepted".encode("utf-8") # convert string to bytes
        # convert and send accept response to the client
        #client_socket.send(response)

    # close connection socket with the client
    client_socket.close()
    print("Connection to client closed")
    # close server socket
    server.close()


run_server()


###prediction request functions

###bad prediction request
