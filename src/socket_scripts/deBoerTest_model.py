import socket
import json
import numpy as np
import random
import base64
## model specific checks that cause a "prediction_request_failed" error
def check_seqs_specifications(sequences):
    max_length = 2000
    for sequence in sequences[0]:
        value = sequences[0][sequence]
        key = sequence

        if len(value) > 2000:
            print("length of a sequence in " + key + " is greater than 2000")

        if "N" in value:
            print("sequence in " + key + " has an invalid character present")


def fake_model_point(sequences, json_dict):
    predictions = {}

    for sequence in sequences[0]:
        value = sequences[0][sequence]
        key = sequence
        print(len(value))
        predictions[key] = random.randint(0, 1)
    json_dict['predictions'] = [predictions]
    return(json_dict)

def fake_model_track(sequences, json_dict):
    predictions = {}

    for sequence in sequences[0]:
        value = sequences[0][sequence]
        key = sequence
        predictions[key] = list(np.random.randint(low = 0,high=50,size=100))

    json_dict['predictions'] = [predictions]

    return(json_dict)

def fake_model_interaction_matrix(sequences, json_dict):
    predictions = {}

    for sequence in sequences[0]:
        value = sequences[0][sequence]
        key = sequence
        interaction_matrix = np.random.randint(10, size=(3, 3))
        predictions[key] = base64.b64encode(np.random.randint(10, size=(3, 3)))

    json_dict['predictions'] = [predictions]
    return(json_dict)
