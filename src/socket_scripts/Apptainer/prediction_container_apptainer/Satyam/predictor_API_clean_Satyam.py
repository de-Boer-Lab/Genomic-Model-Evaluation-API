#Oct 30th, 2024
import socket
import json
import numpy as np
import random
import base64
import sys
import os
import struct
os.chdir('/home/satyam03/scratch_satyam03/Genomic-Model-Evaluation-API/src/socket_scripts/Apptainer/prediction_container_apptainer')
# os.chdir('/Users/ishika/Desktop/API/Genomic-Model-Evaluation-API/src/socket_scripts/Apptainer/prediction_container_apptainer/')
from error_message_functions_updated import *
from deBoerTest_model import *
import argparse

# Define constants
BYTESIZE = 100
ENCODER = "utf-8"

def run_server():
    parser = argparse.ArgumentParser(description='Socket Error Examples')
    parser.add_argument('--host', action="store", dest="host",required=True, help='predictor server ip')
    parser.add_argument('--port', action="store", dest="port", type=int,required=True, help='predictor server port')
    # parser.add_argument('--host_cell_type_matcher', action="store", dest="host_cell_type_matcher",required=False, help='cell type matching ip address')
    # parser.add_argument('--port_cell_type_matcher', action="store", dest="port_cell_type_matcher", type=int,required=False, help='cell type matching port')

    given_args = parser.parse_args()
    evaluator_ip = given_args.host
    evaluator_port = given_args.port
    #cell_type_matcher_ip = given_args.host_cell_type_matcher
    #cell_type_matcher_port = given_args.port_cell_type_matcher

    #create error object
    json_return_error = {}

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind the socket to a specific address and port
    server.bind((evaluator_ip, evaluator_port))
    # listen for incoming connections
    server.listen(0)
    print(f"Listening on {evaluator_ip}:{evaluator_port}")

    # accept incoming connections
    client_socket, client_address = server.accept()
    #client_socket.settimeout(20)
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")


    # #receive JSON from evaluator
    # packets = []

    while True:
        # Before receiving JSON from Evaluator
        # Receive length of the incoming JSON message (4-byte integer)
        # Can change to 8-byte integer by changing .recv(4) to .recv(8)
        # and replacing format string '>I' to '>Q'
        data = b'' # Initialize data to store a new message on each iteration

        # LENGTH PREFIXING
        try:
            raw_msglen = client_socket.recv(4)
            if not raw_msglen:
                print("Failed to receive message length. Closing connection.")
                client_socket.close()
                break # Exit the loop if no message length is received

            # Unpack meesage length from 4 bytes
            msglen = struct.unpack('>I', raw_msglen)[0]
            print(f"Expecting {msglen} bytes of data from the Evaluator.")
            # Can comment out print commands other than for errors

            # Now we want to receive the actual JSON in packets
            while len(data) < msglen:
                packet = client_socket.recv(min(BYTESIZE, msglen-len(data)))
                if not packet:
                    print("Connection closed unexpectedly.")
                    break
                data += packet
                print(f"Received packet of {len(packet)} bytes, total received: {len(data)} bytes")

            # Decode and display the received data if all of it is received
            if len(data) == msglen:
                print("Evaluator request:", data.decode(ENCODER))
                break
            else:
                print("Data received was incomplete or corrupted.")
                break

        except Exception as e:
                print(f"Error while receiving data: {e}")
                client_socket.close()
                break  # Break the loop on exception

        # try:
        #     evaluator_request = client_socket.recv(BYTESIZE)
        #     print(evaluator_request)
        #     if evaluator_request == b"":
        #         print("HI")
        #         break
        #     packets.append(evaluator_request)
        # except socket.timeout:
        #     break

    # evaluator_request_full = b"".join(packets)
# ---------------------- %%%%%%%---------------
    evaluator_request_full = data
    evaluator_json = evaluator_request_full.decode(ENCODER)
    evaluator_json = json.loads(evaluator_json)

    #group these functions
    json_return_error = {'bad_prediction_request': []}

    #if only a "help" was requested return the predictor information file
    if evaluator_json['request'] == "help":
        print("HERE")
        #model builder should specify the path to their help files
        help_file = "/Users/ishika/Desktop/API/Genomic-Model-Evaluation-API/examples/helpExample/predictor_message_onlyINFO_final.json"
        jsonResult_help = json.load(open(help_file))
        jsonResult_help = json.dumps(jsonResult_help)
        #send the evaluator json
        try:
            client_socket.send(jsonResult_help.encode(ENCODER)[:BYTESIZE])
        except socket.error as e:
            print("server_error: Error sending help_file: %s" % e)
            sys.exit(1)
    #re-usable error checking functions
    json_return_error = check_mandatory_keys(evaluator_json.keys(), json_return_error)
    json_return_error = check_request(evaluator_json['request'], json_return_error)
    json_return_error = check_prediction_task_mandatory_keys(evaluator_json['prediction_tasks'], json_return_error)
    #if any of the mandatory keys are missing immediately return an error to the evaluator
    if any(json_return_error.values()) == True:
        json_string = json.dumps(json_return_error)
        try:
            client_socket.send(json_string.encode(ENCODER)[:BYTESIZE])
            sys.exit(1)
        except socket.error as e:
            print ("server_error: Error sending error_file: %s" % e)
            sys.exit(1)
    else:
        json_return_error = check_key_values_readout(evaluator_json['readout'], json_return_error)
        json_return_error = check_prediction_task_name(evaluator_json['prediction_tasks'], json_return_error)
        json_return_error = check_prediction_task_type(evaluator_json['prediction_tasks'], json_return_error)
        json_return_error = check_prediction_task_cell_type(evaluator_json['prediction_tasks'], json_return_error)
        #json_return_error = check_prediction_task_species(evaluator_json['prediction_tasks'], json_return_error)
        if 'prediction_ranges' in evaluator_json.keys():
            json_return_error = check_seq_ids(evaluator_json['prediction_ranges'], evaluator_json['sequences'], json_return_error)
            json_return_error = check_prediction_ranges(evaluator_json['prediction_ranges'], json_return_error)

        if 'upstream_seq' in evaluator_json.keys() or 'downstream_seq' in evaluator_json.keys():
            json_return_error = check_key_values_upstream_flank(evaluator_json['upstream_seq'], json_return_error)
        if 'downstream_seq' in evaluator_json.keys():
            json_return_error = check_key_values_downstream_flank(evaluator_json['downstream_seq'], json_return_error)

        #if any errors were caught return them all to evaluator
        if any(json_return_error.values()) == True:
            json_string = json.dumps(json_return_error)
            try:
                client_socket.send(json_string.encode(ENCODER)[:BYTESIZE])
                sys.exit(1)
            except socket.error as e:
                print ("server_error: Error sending error_file: %s" % e)
                sys.exit(1)

# ---------------------- %%%%%%%---------------
    #extract sequences to predict
    #check that the sequences meet model specifications
    #otherwise do any other formatting required for the model
    sequences = evaluator_json['sequences']
    #can add any additional error checking functons here
    json_return_error_model = {'prediction_request_failed': {}}
    json_return_error_model = check_seqs_specifications(sequences, json_return_error_model)

    #if anything is caught don't run the model and return to evaluator
    if any(json_return_error_model.values()) == True:
        json_string = json.dumps(json_return_error_model)
        try:
            client_socket.send(json_string.encode(ENCODER)[:BYTESIZE])
        except socket.error as e:
            print ("server_error: Error sending error_file: %s" % e)
            sys.exit(1)

    #start big loop here for all the prediction_tasks
    #connect to cell type matching container
    #cell_type_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #cell_type_socket.connect((cell_type_matcher_ip, cell_type_matcher_port))

    #create JSON to return
    json_return = {'request': evaluator_json['request']}
    #prediction task is an array of objects for all requested tasks
    json_return['prediction_tasks'] = []
    #loop through all the prediction tasks
    for prediction_task in evaluator_json['prediction_tasks']:
        #cell type predictor container is running, send the predictors's cell type and evalutor cell type to it
        #If you want to override the cell type container you can remove the following code
        #Send the predictor and evaluator cell type
        #cell_type_socket.sendall(b'Hello, cell type matcher dude!')
        #cell_type_matcher_return = cell_type_socket.recv(BYTESIZE)

        #The following code will be model specific
        #Sample point prediction model
        #Model builders need to add the appropriate returns here
        current_prediction_task = {'name': prediction_task['name']}

        current_prediction_task['type_requested'] =  prediction_task['type']
        current_prediction_task ['type_actual']  = 'expression'

        current_prediction_task['cell_type_requested'] = prediction_task['cell_type']
        current_prediction_task['cell_type_actual'] =  'ishika_cell'

        current_prediction_task['scale_prediction_requested'] =  prediction_task['scale']
        current_prediction_task['scale_prediction_actual']  = 'linear'

        current_prediction_task['species_requested']  = prediction_task['species']
        current_prediction_task['species_actual']  = 'homo_sapiens'

        #add predictions dictionary to the JSON
        current_prediction_task = fake_model_point(sequences, current_prediction_task)
        #append results for current prediction task to the main JSON object
        json_return['prediction_tasks'].append(current_prediction_task)
    #convert dictionary to JSON object and send back to evaluator
    json_string = json.dumps(json_return)
    try:
        client_socket.send(json_string.encode(ENCODER)[:BYTESIZE])
    except socket.error as e:
        print ("server_error: Error sending predictor_file: %s" % e)
        sys.exit(1)
# ---------------------- %%%%%%%---------------

    # close connection socket with the client
    client_socket.close()
    print("Connection to client closed")
    # close server socket
    server.close()

run_server()
