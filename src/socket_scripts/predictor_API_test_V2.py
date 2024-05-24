import socket
import json
import numpy as np
import random
import base64
import sys
import os
os.chdir('/Users/ishika/Desktop/API/Genomic-Model-Evaluation-API/src/socket_scripts/')
from error_messages import *
from deBoerTest_model import *


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
    #while True:
    request = client_socket.recv(1024)
    print(request)
        #gets the evaluator json file
    evaluator_json = request.decode("utf-8") # convert bytes to string
    evaluator_json = json.loads(evaluator_json)
        #check the evaluator_json
        # #run error checking functions for bad prediction request
        # evaluator_file = open('/Users/ishika/Desktop/API/Genomic-Model-Evaluation-API/examples/sampleRequest1/evaluator_message.json')
        # #this will catch json formatting errors
        # try:
        #     evaluator_json = json.load(evaluator_file)
        #     print(evaluator_json)
        # except json.JSONDecodeError as e:
        #     print("Invalid JSON syntax:", e)
        #
    #group these functions
    json_return_error = {'bad_prediction_request': []}
    #print(json_return_error)
    json_return_error = check_mandatory_keys(evaluator_json.keys(), json_return_error)
    #print(json_return_error)
    if any(json_return_error.values()) == True:
        json_string = json.dumps(json_return_error,ensure_ascii=False, indent=4)
        try:
            client_socket.send(json_string.encode("utf-8")[:1024])
        except socket.error as e:
            print ("server_error: Error sending error_file: %s" % e)
            sys.exit(1)
    else:
        #return here
        json_return_error = check_task(evaluator_json['task'], json_return_error)
        json_return_error = check_prediction_types(evaluator_json['prediction_types'], json_return_error)
        #print(json_return_error)
        json_return_error = check_cell_types_length(evaluator_json['prediction_types'], evaluator_json['cell_types'], json_return_error)
        json_return_error = check_key_values_readout(evaluator_json['readout'], json_return_error)
        #print(json_return_error)
        if 'scale' in evaluator_json.keys():
            json_return_error = check_scale_length(evaluator_json['prediction_types'], evaluator_json['scale'], json_return_error)
        if 'prediction_ranges' in evaluator_json.keys():
            json_return_error = check_seq_ids(evaluator_json['prediction_ranges'], evaluator_json['sequences'], json_return_error)
            json_return_error = check_prediction_ranges(evaluator_json['prediction_ranges'], json_return_error)
        if 'strand' in evaluator_json.keys():
            json_return_error = check_key_values_strand(evaluator_json['strand'], json_return_error)
        if 'scale' in evaluator_json.keys():
            json_return_error = check_key_values_scale(evaluator_json['scale'], evaluator_json['prediction_types'], json_return_error)
        if 'upstream_seq' in evaluator_json.keys() or 'downstream_seq' in evaluator_json.keys():
            json_return_error = check_key_values_upstream_flank(evaluator_json['upstream_seq'], json_return_error)
        if 'downstream_seq' in evaluator_json.keys():
            json_return_error = check_key_values_downstream_flank(evaluator_json['downstream_seq'], json_return_error)

    #if any errors were caught return to evaluator
    if any(json_return_error.values()) == True:
        json_string = json.dumps(json_return_error,ensure_ascii=False, indent=4)
        try:
            client_socket.send(json_string.encode("utf-8")[:1024])
        except socket.error as e:
            print ("server_error: Error sending error_file: %s" % e)
            sys.exit(1)


    #run the predictor container
    #check each sequence based on the model's specifications for
    #what characters and length is allowed for the sequence
    ##run error checking functions for prediction_request_failed

    #Send the sequences to the model
    #Return crap for each sequence regardless of what task is requested

    #information to return to evaluator
    json_return = {'task': evaluator_json['task'], 'prediction_types': evaluator_json['prediction_types']}
    json_return
    json_return_error_model = {'prediction_request_failed': {}}

    if evaluator_json['task'] == "help":
        help_file = "/Users/ishika/Desktop/API/Genomic-Model-Evaluation-API/examples/helpExample/predictor_message_onlyINFO_final.json"
        #send the evaluator json
        try:
            client_socket.send(help_file.encode("utf-8")[:1024])
        except socket.error as e:
            print("server_error: Error sending help_file: %s" % e)
            sys.exit(1)
    sequences = evaluator_json['sequences']
    if evaluator_json['readout'] == "point":
        #model bin size specifications
        json_return['bin_size'] = 1

        ## fake call cell type container
        json_return['cell_types'] = ['HepG2']
        json_return['aggregation'] = "mean of replicates"

        json_return_error_model = check_seqs_specifications(sequences, json_return_error_model)
        if any(json_return_error_model.values()) == True:
            json_string = json.dumps(json_return_error_model,ensure_ascii=False, indent=4)
            try:
                client_socket.send(json_string.encode("utf-8")[:1024])
            except socket.error as e:
                print ("server_error: Error sending error_file: %s" % e)
                sys.exit(1)


        json_return = fake_model_point(sequences, json_return)

        json_string = json.dumps(json_return)
        print(json_return)
        try:
            client_socket.send(json_string.encode("utf-8")[:1024])
        except socket.error as e:
            print ("Error sending predictor_file: %s" % e)
            sys.exit(1)

    if evaluator_json['readout'] == "track":
        #model bin size specifications
        json_return['bin_size'] = 1

        ## fake call cell type container
        json_return['cell_types'] = ['HepG2']
        json_return['aggregation'] = "mean of replicates"


        json_return_error_model = check_seqs_specifications(sequences, json_return_error_model)
        if any(json_return_error_model.values()) == True:
            json_string = json.dumps(json_return_error_model,ensure_ascii=False, indent=4)
            try:
                client_socket.send(json_string.encode("utf-8")[:1024])
            except socket.error as e:
                print ("server_error: Error sending error_file: %s" % e)
                sys.exit(1)


        json_return = fake_model_track(sequences, json_return)
        json_string = json.dumps(json_return,
                                 ensure_ascii=False, indent=4)
        try:
            client_socket.send(json_string.encode("utf-8")[:1024])
        except socket.error as e:
            print ("server_error: Error sending predictor_file: %s" % e)
            sys.exit(1)

    if evaluator_json['readout'] == "interaction_matrix":
                #model bin size specifications
        json_return['bin_size'] = 1

        ## fake call cell type container
        #moved out of the model
        json_return['cell_types'] = ['HepG2']
        json_return['aggregation'] = "mean of replicates"

        json_return_error_model = check_seqs_specifications(sequences, json_return_error_model)

        if any(json_return_error_model.values()) == True:
            json_string = json.dumps(json_return_error_model,ensure_ascii=False, indent=4)
            try:
                client_socket.send(json_string.encode("utf-8")[:1024])
            except socket.error as e:
                print ("server_error: Error sending error_file: %s" % e)
                sys.exit(1)

        json_return = fake_model_interaction_matrix(sequences, json_return)
        json_string = json.dumps(json_return,
                                 ensure_ascii=False, indent=4)
        try:
            client_socket.send(json_string.encode("utf-8")[:1024])
        except socket.error as e:
            print ("server_error: Error sending predictor_file: %s" % e)
            sys.exit(1)

    #Format the json output file and send back to evaluator
    # if we receive "close" from the client, then we break
    # out of the loop and close the conneciton
    # if request.lower() == "close":
    #     # send response to the client which acknowledges that the
    #     # connection should be closed and break out of the loop
    #     client_socket.send("closed".encode("utf-8"))
    #     break

    # jsonReceived = c.recv(1024)
    # print(jsonReceived)
    # print(f"Received: {request}")
    # response = "accepted".encode("utf-8") # convert string to bytes
    # convert and send accept response to the client
    # client_socket.send(response)

    # close connection socket with the client
    client_socket.close()
    print("Connection to client closed")
    # close server socket
    server.close()

run_server()
