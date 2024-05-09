import socket
import json
import numpy as np

def run_server():
    # create a socket object

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

        # try:
        #     data = json.loads(json_data)
        #     print(data)
        # except json.JSONDecodeError as e:
        #     print("Invalid JSON syntax:", e)
        #
        evaluator_file = open('/Users/ishika/Desktop/API/Genomic-Model-Evaluation-API/examples/sampleRequest2/evaluator_message_final.json')
        evaluator_json = json.load(evaluator_file)
        print(evaluator_json)


        evaluator_json['task']
        evaluator_json["sequences"][0].keys()
        evaluator_json["prediction_types"][0]
        evaluator_json["prediction_types"]
        evaluator_json.get("seq1")

        #run the predictor container
        #check each sequence based on the model's specifications for
        #what characters and length is allowed for the sequence
        ##run error checking functions for prediction_request_failed

        #Send the sequences to the model

        #Return crap for each sequence regardless of what task is requested

        #Format the json output file and send back to evaluator

        print(request)
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

#check the the mandatory_keys exsist in the .json files
prediction_types = evaluator_json["prediction_types"]
evaluator_keys = list(evaluator_json.keys())
check_keys(evaluator_keys, prediction_types)

def check_keys(evaluator_keys, prediction_types):

    # if "binding_types" in prediction_types:
    #     mandatory_keys = ["task", "readout", "prediction_types", "binding_types","cell_types", "sequences"]
    #     np.in1d(mandatory_keys, evaluator_keys).all()
    #     missing = list(sorted(set(mandatory_keys) - set(evaluator_keys)))
    #     if not missing:
    #         return("correct keys")
    #     else:
    #         return("The following keys are missing from the json" + str(missing))
    # else:
    mandatory_keys = ["task", "readout", "prediction_types", "cell_types", "sequences"]
    np.in1d(mandatory_keys, evaluator_keys).all()
    missing = list(sorted(set(mandatory_keys) - set(evaluator_keys)))
    if not missing:
        return("correct keys")
    else:
        return("The following keys are missing from the json" + str(missing))

#check the task requested is correct
task_types = evaluator_json["task"]
check_task(task_types)
def check_task(task_types):

    task_options = ["predict", "interpret", "help"]

    if task_types not in task_options:

        return("task requested is not recognized. Please choose from ['predict', 'interpret', 'help']")

    else:
        return("task requested exists in the predictor")

prediction_types = evaluator_json["prediction_types"]
check_prediction_types(prediction_types)
def check_prediction_types(prediction_types):

    prediction_types_options = ["accessibility", "expression", "chromatin_confirmation"]
    for prediction_type in prediction_types:
        if prediction_type in prediction_types_options or prediction_type.startswith('binding_'):
            print()
        else:
            print("prediction type " + str(prediction_type) + " is not recognized")

#check duplicate sequence ids - this needs to be fixed since the duplicates just get overwritten
#sequence_ids = list(evaluator_json["sequences"][0].keys())
# check_seq_ids(sequence_ids)
# def check_seq_ids(sequence_ids):
#     if len(set(sequence_ids)) != len(sequence_ids):
#
#         return("duplicate sequence ids in 'sequences'.")
#
#     else:
#         return("sequence_ids are all unique")


evaluator_file = open('/Users/ishika/Desktop/API/Genomic-Model-Evaluation-API/examples/sampleRequest2/evaluator_message_final.json')
evaluator_json = json.load(evaluator_file)
### check that prediction_ranges are integers and subarrays are 2 elemnts each
prediction_ranges = evaluator_json["prediction_ranges"]
check_prediction_ranges(prediction_ranges)
def check_prediction_ranges(prediction_ranges):

    for i in prediction_ranges[0]:
        value = prediction_ranges[0][i]
        key = i

        if any(isinstance(el, list) for el in value) == True:
            for sub_list in value:
                 if len(sub_list) != 2:
                     print("length of a sub-array in " + key + " is greater than 2")
                 for item in sub_list:
                     if isinstance(item, int) == True:
                         pass
                     else:
                         print("value in " + key + " key is not an integer")

        else:
            if len(value) > 2:
                print("length array in " + key+ " is greater than 2")

            for item in value:
                if isinstance(item, int) == True:
                    pass
                else:
                    print("value in " + key + " key is not an integer")

##check that seqids have valid characters
## apparently this is done by default in .json loads
#it works for some but not all

#check that length of prediction_types should be the same as length of cell_types or only 1 value
prediction_types = evaluator_json["prediction_types"]
cell_types = evaluator_json["cell_types"]
check_cell_types_length(prediction_types, cell_types)

def check_cell_types_length(prediction_types, cell_types):

    if ((len(prediction_types) == len(cell_types)) or (len(cell_types) == 1)):
        pass
    else:
        print("length of prediction_types should be the same as length of cell_types or only 1 value")


#check that keys in sequences match those in prediction ranges
prediction_ranges = evaluator_json["prediction_ranges"]
sequences = evaluator_json["sequences"]
check_seq_ids(prediction_ranges, sequences)

def check_seq_ids(prediction_ranges, sequences):
    if prediction_ranges[0].keys() == sequences[0].keys():
        pass
    else:
        print("sequence ids in prediction_ranges do not match those in sequences")



###server error
