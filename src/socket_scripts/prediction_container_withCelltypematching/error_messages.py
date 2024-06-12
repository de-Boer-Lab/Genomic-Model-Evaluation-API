import socket
import json
import numpy as np
import random
import base64
#check the the mandatory_keys exsist in the .json files

def check_mandatory_keys(evaluator_keys, json_return_error):

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
        pass
    else:
        json_return_error['bad_prediction_request'].append(("The following keys are missing from the json" + str(missing)))
    return(json_return_error)
#check the task requested is correct

def check_task(task_types, json_return_error):

    task_options = ["predict", "interpret", "help"]

    if task_types not in task_options:
        json_return_error['bad_prediction_request'].append(("task requested is not recognized. Please choose from ['predict', 'interpret', 'help']"))

    else:
        pass
        #return("task requested exists in the predictor")

    if isinstance(task_types, str) == True:
        pass
    else:
        json_return_error['bad_prediction_request'].append("'task' value should be a string")

    if type(task_types) == list:
        json_return_error['bad_prediction_request'].append("'task' should only have 1 value")
    else:
        pass

    return(json_return_error)

def check_prediction_types(prediction_types, json_return_error):

    prediction_types_options = ["accessibility", "expression", "chromatin_confirmation"]
    for prediction_type in prediction_types:
        if prediction_type in prediction_types_options or prediction_type.startswith('binding_'):
            pass
        else:
            json_return_error['bad_prediction_request'].append("prediction type " + str(prediction_type) + " is not recognized")
    return(json_return_error)

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

def check_prediction_ranges(prediction_ranges, json_return_error):
    for i in prediction_ranges[0]:
        value = prediction_ranges[0][i]
        key = i

        if any(isinstance(el, list) for el in value) == True:
            for sub_list in value:
                 if len(sub_list) != 2:
                     json_return_error['bad_prediction_request'].append("length of a sub-array in " + key + " is greater than 2")
                 for item in sub_list:
                     if isinstance(item, int) == True:
                         pass
                     else:
                         json_return_error['bad_prediction_request'].append("value in " + key + " key is not an integer")
        else:
            if len(value) > 2:
                json_return_error['bad_prediction_request'].append("length array in " + key+ " is greater than 2")

            for item in value:
                if isinstance(item, int) == True:
                    pass
                else:
                    json_return_error['bad_prediction_request'].append("value in " + key + " key is not an integer")
        return(json_return_error)
##check that seqids have valid characters
## apparently this is done by default in .json loads
#it works for some but not all

#check that length of prediction_types should be the same as length of cell_types or only 1 value
def check_cell_types_length(prediction_types, cell_types, json_return_error):

    if ((len(prediction_types) == len(cell_types)) or (len(cell_types) == 1)):
        pass
    else:
        json_return_error['bad_prediction_request'].append("length of prediction_types should be the same as length of cell_types or only 1 value")
    return(json_return_error)

def check_scale_length(prediction_types, scale, json_return_error):

    if ((len(prediction_types) == len(scale)) or (len(scale) == 1)):
        pass
    else:
        json_return_error['bad_prediction_request'].append("length of scale should be the same as length of cell_types/prediction_types or only 1 value")
    return(json_return_error)
#check that keys in sequences match those in prediction ranges

def check_seq_ids(prediction_ranges, sequences, json_return_error):
    if prediction_ranges[0].keys() == sequences[0].keys():
        pass
    else:
        json_return_error['bad_prediction_request'].append("sequence ids in prediction_ranges do not match those in sequences")
    return(json_return_error)
# evaluator_file = open('/Users/ishika/Desktop/API/Genomic-Model-Evaluation-API/examples/sampleRequest2/evaluator_message_final.json')
# evaluator_json = json.load(evaluator_file)
# check_key_values_readout(evaluator_json['readout'])
# type(evaluator_json['readout'])
def check_key_values_readout(readout_value, json_return_error):
    readout_options = ["point","track", "interaction_matrix"]

    if readout_value not in readout_options:

        json_return_error['bad_prediction_request'].append("readout requested is not recognized. Please choose from ['point', 'track', 'interaction_matrix']")
    else:
        pass
    if isinstance(readout_value, str) == True:
        pass
    else:
        json_return_error['bad_prediction_request'].append("'readout' value should be a string")

    if type(readout_value) == list:
        json_return_error['bad_prediction_request'].append("'readout' should only have 1 value")

    else:
        pass
    return(json_return_error)

def check_key_values_strand(strand_value, json_return_error):
    strand_options = ["positive","negative"]

    if strand_value not in strand_options:
        json_return_error['bad_prediction_request'].append("strand requested is not recognized. Please choose from ['positive', 'negative']")

    else:
        pass
    if isinstance(strand_value, str) == True:
        pass
    else:
        json_return_error['bad_prediction_request'].append("'strand' value should be a string")

    if type(strand_value) == list:
        json_return_error['bad_prediction_request'].append("'strand' should only have 1 value")
    else:
        pass
    return(json_return_error)

def check_key_values_scale(scale_values, prediction_types, json_return_error):
    scale_options = ["log","linear"]
    for scale_value in scale_values:
        if scale_value in scale_options:
            pass
        else:
            json_return_error['bad_prediction_request'].append("scale requested is not recognized. Please choose from ['log', 'linear']")

            if isinstance(scale_value, str) == True:
                pass
            else:
                json_return_error['bad_prediction_request'].append("'scale' value should be a string")

    if len(scale_values) != len(prediction_types):
        json_return_error['bad_prediction_request'].append("length of `scale_prediction` should be the same as `prediction_types`")
    return(json_return_error)

def check_key_values_upstream_flank(upstream_seq, json_return_error):

    if isinstance(upstream_seq, str) == True:
        pass
    else:
        json_return_error['bad_prediction_request'].append("'upstream_seq' value should be a string")
    if type(upstream_seq) == list:
        json_return_error['bad_prediction_request'].append("'upstream_seq' should only have 1 value")
    else:
        pass
    return(json_return_error)



def check_key_values_downstream_flank(downstream_seq, json_return_error):

    if isinstance(downstream_seq, str) == True:
        pass
    else:
        json_return_error['bad_prediction_request'].append("'downstream_seq' value should be a string")
    if type(downstream_seq) == list:
        json_return_error['bad_prediction_request'].append("'downstream_seq' should only have 1 value")
    else:
        pass
    return(json_return_error)
