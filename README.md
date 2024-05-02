---
---
---

# Genomic Model Evaluation API

### API Reference

This Application Programming Interface (API) was designed for the functional genomics community to create seamless communication across pre-trained models and genomics datasets. It is a product of the feedback from many model and dataset experts and our hope is that it allows for long-lasting benchmarking of models. Models and datasets communicate via a set of predefined protocols through APIs. The common protocol enables any model to communicate with any dataset (although not all combinations may make sense).

The evaluators (dataset APIs) will make prediction requests in the standard format (seen below) to the predictors (model APIs), which then return the predictions to the evaluator in a standard format, enabling the evaluators to calculate the model’s performance. Each of the evaluators and predictors will be containerized using Singularity (more details below).

The communication protocol below covers some of the mandatory parameters required for the API. There are also some optional parameters for specific prediction requests. 

For this effort to succeed we encourage data and model experts to provide us with feedback and support (via contributing evalutors and predictors). Since dataset creators are the experts in their dataset, they are most qualified to decide how these models should be evaluated on their data. Meanwhile, model creators are best qualified for deciding how the model should be used for the inference tasks. Accordingly, the responsibilities for adding the new datasets and models would fall on their creators. Once they set up the intial Being able to easily compare results across different datasets and models would accelerate the improvement of genomics models, motivate novel functional genomic benchmarks, and provide a more nuanced understanding of model abilities.

If you would like to be involved we encourage you to use this API with your own models and datasets and submit to the Github repo list (add link). If you have critiques or feedback please reach out to [ishika.luthra\@ubc.ca](mailto:ishika.luthra@ubc.ca)

![](./src/API_V2.png)

### Communication protocol

Using the standardized communication format each predictor will receive information in the same format from any evalutor. Each predictor also returns the predictions in the same format which enables the community to easily compare different model's predictions for the same dataset or evaluate a model on multiple different types of datasets very quickly. 

The only files that are exchanged between the evaluators and predictors are .json files, a commonly used file format for sending and receiving information in a standard format. Data in the .json files is stored in the following format: `"keys": "value"`, where the value can be strings, numbers, objects, arrays, booleans or null. We have outlined below the mandatory "keys" required for communication between the evaluator and predictor to occur. Certain "keys" have a fixed set of "values" that can be used while others are up to the evaluator builder. 

The files and communiction between APIs is done using python sockets. Scripts for these can be found in `\src\socket_scripts\`.

Examples of evaluator and predictor messages can be found in `\examples\json\` folder. 

Examples of containerized evaluators and predictors can be found in `\examples\containers\` folder. 

#### Communication protocol example

<span style="color: #FF69B4;">Hi my name is "Predictor"! My job is to wait and listen for a "Evaluator" to ask me to do something.</span>

<span style="color: #87CEEB;">Hello I'm an "Evaluator"! I'm sending you a .json file, could you please predict the accessbility of these sequences?</span>

<span style="color: #FF69B4;">Sure thing :) Here you go - i'm sending you a .json file back with all the predictions. </span>
                      
### An example for how issue a request from the predictor

The example below outlines an easy test communication between an evaluator (with random sequences) and a predictor (that will generate random predictions for any task you request). 

TO ADD

`python`

### Evaluator request message

| Key                 | Value type - Required/Optional                   | Description: Value options                                                                                                                                                                                                                                                                                                                                                  | Example                                                                                                                                                                                                 |
|--------------|--------------|-------------------------------|--------------|
| `task`              | `string` - Required                 | What task you are asking the predictor to complete : ["predict", "interpret", "help"]                                                                                                                                                                                                                                                                         | "task": "predict"                                                                                                                                                                                       |
| `readout`           | `string` - Required                | Type of readout that is requested from the predictor : ["point","track", "interaction_matrix"]                                                                                                                                                                                                                                                                              | "readout": "track"                                                                                                                                                                                      |
| `prediction_types`  | `array of strings` - Required        | What you want predicted for each cell type. Array needs to be the same length as `cell_types` or 1 value that is applied to all values in `cell_types` : ["accessibility", "binding" , expression", "chromatin_confirmation"]                                                                                                                                                                                          | "prediction_types": ["expression", "binding", "accessibility", "binding"]                                                                                                                                          |
| `binding_types`  | `array of strings` - Required if "binding" is one of the values for `prediction_types`      | What type of "binding" you want the model to predict. Array needs to be the same length as the number of "binding" prediction types requested or 1 value that is applied to all binding values.                                                                                                                                                           | "binding_types" : ["H3K4me3", "CTCF"]                                                                                                                                          |
| `cell_types`        | `array of strings` - Required       | What cell type do you want for each `prediction_types`. Array needs to be the same length as `prediction_types` or only 1 value which will default for all `prediction_types`                                                                                                                                                                                | "cell_types" : ["HEPG2", "K562", "K562", "iPSC"]                                                                                                                                                                 |
| `scale`             | `array of strings` - Optional                 | How would you like the predictions scaled upon return (if at all). Array needs to be the same length as `prediction_types` : ["linear", "log"]                                                                                                                                                                                                                                                                         | "scale" : ["log", "log", "linear", "linear"]                                                                                                                                                                                           |
| `strand`            | `string`- Optional                  | Which strand would you like to be predicted  : ["positive", "negative"]                                                                                                                                                                                                                                                                                       | "strand": "positive"                                                                                                                                                                                     |
| `upstream_seq`      | `string`- Optional                  | Upstream flanking sequences to add to each sequence.                                                                                                                                                                                                                                                                                       | "upstream_seq" : "AATTA"                                                                                                                                                                                |
| `downstream_seq`    | `string`- Optional                  | Downstream flanking sequences to add to each sequence.                                                                                                                                                                                                                                                                                    | "downstream_seq" : "CCCAAAA"                                                                                                                                                                            |
| `sequences`         | `array of strings` - Required       | A collection of key-value pairs. Array of sequences with unique sequence ids - any characters [A-Z][a-z][0-9][-.\_\~#\@%^&\*()]. The sequence ids are matched to the predictor returned sequence ids automatically by predictor                                                                                                                              | "sequences" : [<br> {<br>   "seq1" : "ATGC...",<br>   "seq2" : "ATGC...",<br>  "random_seq" : "ATGC...",<br>  "enhancer" : "ATGC...",<br>  "control" : "ATGC..." <br> }<br>]                                   |
| `prediction_ranges` | `multi-dimensional array`- Optional | A collection of key-value pairs, where the value is a multi/single-dimensional array based on what regions you want included in the predictions for each sequence. Sub-arrays of 2 integers mark the start and end location of the range of prediction you are interested in and you can have multiple starts and stops per sequence. Keys should be identical to the sequence ids.| "prediction_ranges" : [<br>  {<br>   "seq1" : [0,1000] ,<br>   "seq2" : [100,110],<br>  "random_seq" : [ <br>    [0,10],<br>    [15,100] <br>   ],<br>  "enhancer" :    [210,500],<br>  "control" : [] <br> }<br>] |

### Predictor return message

| Key                | Value type - Required/Optional             | Description                                                                                                                                                                                                | Example Values                |
|---------------|---------------|-----------------------------|---------------|
| `task`             | `string`- Required           | What task was completed by the model                                                                                                                                                                       | "task" : "predict"      |
| `scale_prediction` | `array of strings` - Optional            | How did the predictor scale the predictions (if at all). Array needs to be the same length as `prediction_types`.                                                                                                                                                    | "scale" : ["log", "log", "linear"]          |
| `cell_types`       | `array of strings`- Required | Cell types used by the predictor for each of the `prediction_types` or one 1 cell type for all. Predictor developer can choose to use cell type/cell line ontology container which will returned the closest matched cell type that the predictor has.                                   | "cell_types" : ["HEPG2"] |
| `aggregation`      | `string`- Optional           | How replicate tracks were aggregated for each of the `prediction_types`. Array needs to be the same length as `prediction_types`.                                                                                                                                     | "aggregation" : ["mean", "mean", "mean"]   |
| `predictions`      | `Array of floats/integers`- Required    | A collection of key-value pairs. Array of predictions can be a single value or list of values for track predictions. The sequence ids are matched to the evaluator sequence ids automatically by predictor |"predictions" : [<br> {<br>   "seq1" :  [12.2, 5, 6, ..],<br>   "seq2" : [1.1, 12, 0.00, ..],<br>  "random_seq" : [100.1, 50, 0.5, ..],<br>  "enhancer" : [4, 3.0, 0.001, ..],<br>  "control" : [0, 0, 0, ..] <br> }<br>]<br>                         |

### Retrive information about predictor classes

Any evaluator can retrieve information from a predictor by asking for `help` in the `task` key. This will return a `.json` file that is written by predictor builders. The keys attached below are mandatory for the communication

Message sent by evalutor:

| Key: Value    | Value type- Required/Optional  |Description                                                                 |
|--------------|--------------|---------------------|
| "task" : "help" | `string`- Required| Retrieve basis information about the predictor (written by model developers) |

Message returned by predictor:

| Key                     | Value type     | Description       | Example Values |
|---------------|---------------|-------------------------------------------|----------|
| `model`                 | `string`- Optional  | Model name                                                                                                         | "model" : "deBoer Lab test" |
| `version`               | `string`- Optional  | Information about version of model                                                                                 | "version" : "2.2"|
| `build_date`            | `string`- Optional  | Date the predictor container was built - to track potential rebuilds                                               | "build_date" : "Aug 20, 2024"|
| `features`              | `array of strings`- Optional   | List of features that the model predicts for each cell types.                                                 | "features" : [<br> {<br>   "HEPG2" : ["accessibility", "H3K4me3",...],<br>   "iPSC" : ["H3K4me3", "accessbility",...],<br>  "Adult liver" : ["CAGE", "DNase",...] <br>  } <br>] |
| `species`               | `array of strings`- Optional  | Name of species that the model predicts for.                                                   | "species" : ["yeast", "human"]|
| `author`                | `string`- Optional  | Paper author/authors or name of container builder                                                                  |  "author" : "Ishika Luthra" |
| `input_size`            | `Integer`- Optional | Number of base pairs of sequence that the model requires as input                                                  | "input_size" : 500500 |
| `output_size`           | `Integer`- Optional | Length of region that the model predicts across. Can also be one for single prediction models.                  | "output_size" : 100000|
| `resolution`            | `Integer`- Optional | For models that predict across genomic tracks what is the base pair resolution                                     | "resolution" : 10|
| `max_prediction_length` | `Integer`- Optional | What is the maximum sequence length you can provide before the model will no longer be able to handle the sequence | "max_prediction_length" : "2MB"

### Error messages

Error messages that should be returned by the predictors in .json format. Error messages should be returned via one of the 3 possible keys so that the evaluators can "catch" the exception. Values can follow the format described below (any type) or other/additional ones can be added by the predictor builders.

We encourage predictor builders to return error messages in the format show below. Helper functions that have some basic error catching to build off can be found in the `src` folder. 

| Error Message Keys    | Value type |Description                                               | Example Values                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|-------------|-------------|----------------------------------------------|---------------------|
| `bad_prediction_request`    | `array of strings` |Request was unacceptable - Predictor did not run          | •.json file is formatted incorrectly <br> •mandatory key `x` is missing in .json <br> •`task` requested is not recognized. Please choose from the following list `["predict", "interpret", "help"]` <br> •duplicate sequence ids in `sequences`: sequence id `y` is duplicated <br> •`prediction_ranges` are required to be integers <br> •length of `prediction_types` should be the same as length of `cell_types` or only 1 value <br> •sequence ids in `prediction_ranges` do not match those in `sequences` <br> •length of each sub-array in `prediction_ranges` should not be greater than 2 <br> • sequence id `z` has an invalid character present <br> |
| `prediction_request_failed` | `array of strings` |Evaluator message was valid but prediction was incomplete | • "seq_z" in `sequences` has an invalid character present <br> • predictor cannot handle sequence lengths this large <br>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `server_error`              | `array of strings` | Backend issue                                             | •socket communication failed <br> •wifi error <br> •memory error (eg. due to large batch size, due to large .json file)                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |

### To create standarized plots

To create plots similar to those included in our examples once you have completed your prediction requests use `python`.

TO DO
