import socket
import json
import numpy as np
import random
import base64
#check the the mandatory_keys exsist in the .json files

def check_mandatory_keys(evaluator_keys):

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
def check_task(task_types):

    task_options = ["predict", "interpret", "help"]

    if task_types not in task_options:

        return("task requested is not recognized. Please choose from ['predict', 'interpret', 'help']")

    else:
        return("task requested exists in the predictor")

    if isinstance(task_types, str) == True:
        pass
    else:
        print("'task' value should be a string")

    if len(task_types, str) == 1:
        pass
    else:
        print("'task' should only have 1 value")

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



### check that prediction_ranges are integers and subarrays are 2 elemnts each

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
def check_cell_types_length(prediction_types, cell_types):

    if ((len(prediction_types) == len(cell_types)) or (len(cell_types) == 1)):
        pass
    else:
        print("length of prediction_types should be the same as length of cell_types or only 1 value")


def check_scale_length(prediction_types, scale):

    if ((len(prediction_types) == len(scale)) or (len(scale) == 1)):
        pass
    else:
        print("length of scale should be the same as length of cell_types/prediction_types or only 1 value")

#check that keys in sequences match those in prediction ranges

def check_seq_ids(prediction_ranges, sequences):
    if prediction_ranges[0].keys() == sequences[0].keys():
        pass
    else:
        print("sequence ids in prediction_ranges do not match those in sequences")

# evaluator_file = open('/Users/ishika/Desktop/API/Genomic-Model-Evaluation-API/examples/sampleRequest2/evaluator_message_final.json')
# evaluator_json = json.load(evaluator_file)
# check_key_values_readout(evaluator_json['readout'])
# type(evaluator_json['readout'])
def check_key_values_readout(readout_value):
    readout_options = ["point","track", "interaction_matrix"]

    if readout_value not in readout_options:

        return("readout requested is not recognized. Please choose from ['point', 'track', 'interaction_matrix']")

    else:
        pass
    if isinstance(readout_value, str) == True:
        pass
    else:
        print("'readout' value should be a string")

    if type(readout_value) == list:
        print("'readout' should only have 1 value")
    else:
        pass

def check_key_values_strand(strand_value):
    strand_options = ["positive","negative"]

    if strand_value not in strand_options:

        return("strand requested is not recognized. Please choose from ['positive', 'negative']")

    else:
        pass
    if isinstance(strand_value, str) == True:
        pass
    else:
        print("'strand' value should be a string")

    if type(strand_value) == list:
        print("'strand' should only have 1 value")
    else:
        pass

def check_key_values_scale(scale_value):
    scale_options = ["log","linear"]

    if scale_value not in scale_options:

        return("scale requested is not recognized. Please choose from ['log', 'linear']")

    else:
        pass
    if isinstance(scale_value, str) == True:
        pass
    else:
        print("'scale' value should be a string")

    if type(scale_value) == list:
        print("'scale' should only have 1 value")
    else:
        pass

def check_key_values_flanks(upstream_seq, downstream_seq):

    if isinstance(upstream_seq, str) == True:
        pass
    else:
        print("'upstream_seq' value should be a string")

    if type(scale_value) == list:
        print("'upstream_seq' should only have 1 value")
    else:
        pass

    if isinstance(downstream_seq, str) == True:
        pass
    else:
        print("'downstream_seq' value should be a string")

    if type(downstream_seq) == list:
        print("'downstream_seq' should only have 1 value")
    else:
        pass
