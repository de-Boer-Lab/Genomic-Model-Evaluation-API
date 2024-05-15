---
---
---

# Genomic Model Evaluation API

### API Reference

This Application Programming Interface (API) was designed for the functional genomics community to create seamless communication across pre-trained models and genomics datasets. It is a product of the feedback from many model and dataset experts and our hope is that it allows for long-lasting benchmarking of models. Models and datasets communicate via a set of predefined protocols through APIs. The common protocol enables any model to communicate with any dataset (although not all combinations may make sense).

The evaluators (dataset APIs) will make prediction requests in the standard format (seen below) to the predictors (model APIs), which then return the predictions to the evaluator in a standard format, enabling the evaluators to calculate the model’s performance. Each of the evaluators and predictors will be containerized using Singularity (more details below).

The communication protocol below covers some of the mandatory parameters required for the API. There are also some optional parameters for specific prediction requests. 

For this effort to succeed we encourage data and model experts to provide us with feedback and support (via contributing evalutors and predictors). Since dataset creators are the experts in their dataset, they are most qualified to decide how these models should be evaluated on their data. Meanwhile, model creators are best qualified for deciding how the model should be used for the inference tasks. Accordingly, the responsibilities for adding the new datasets and models would fall on their creators. Once they set up the intial Being able to easily compare results across different datasets and models would accelerate the improvement of genomics models, motivate novel functional genomic benchmarks, and provide a more nuanced understanding of model abilities.

If you would like to be involved we encourage you to use this API with your own models and datasets and submit to the Github repo list (add link). If you have critiques or feedback please reach out to [ishika.luthra\@ubc.ca](mailto:ishika.luthra@ubc.ca). The protocol is still under development, **indicates specific ideas we would like feedback on. 

![](./src/API_V2.png)

### Communication protocol

Using the standardized communication format each predictor will receive information in the same format from any evalutor. Each predictor also returns the predictions in the same format which enables the community to easily compare different model's predictions for the same dataset or evaluate a model on multiple different types of datasets very quickly. 

The only files that are exchanged between the evaluators and predictors are .json files, a commonly used file format for sending and receiving information in a standard format. Data in the .json files is stored in the following format: `"keys": "value"`, where the value can be strings, numbers, objects, arrays, booleans or null. We have outlined below the mandatory "keys" required for communication between the evaluator and predictor to occur. Certain "keys" have a fixed set of "values" that can be used while others are up to the evaluators.

The files and communication between APIs is done using python sockets. Scripts for these can be found in `\src\socket_scripts\`.

Examples of evaluator and predictor messages can be found in `\examples\json\` folder. Formats for json files can be checked using the following link: https://jsonformatter.curiousconcept.com

Examples of containerized evaluators and predictors can be found in `\examples\containers\` folder. 

#### Communication protocol example

P: Hi my name is "Predictor"! My job is to wait and listen for a "Evaluator" to ask me to do something.

E: Hello I'm an "Evaluator"! I'm sending you a .json file, could you please predict the accessbility of these sequences?

P: Sure thing :) One moment please...

P: Psst! Hey CellMatcher! I was asked for cellX, but I have no clue that that is, can I have a little help?

CM: Sure thing! cellX is similar to your cellY, so you should use that for your predictions instead. 

P: Here you go, Evaluator - i'm sending you a .json file back with all the predictions for cellY.
                      
### An example for how issue a request from the predictor

The example below outlines an easy test communication between an evaluator (with random sequences) and a predictor (that will generate random predictions for any task you request). 

TO ADD

`python`

### Evaluator request message

| Key                 | Value type - Required/Optional                   | Description: Value options                                                                                                                                                                                                                                                                                                                                                  | Example                                                                                                                                                                                                 |
|--------------|--------------|-------------------------------|--------------|
| `task`              | `string` - Required                 | What task you are asking the predictor to complete : ["predict", "interpret", "help"]                                                                                                                                                                                                                                                                         | "task": "predict"                                                                                                                                                                                       |
| `readout`           | `string` - Required                | Type of readout that is requested from the predictor : ["point","track", "interaction_matrix"]                                                                                                                                                                                                                                                                              | "readout": "track"                                                                                                                                                                                      |
| `prediction_types`  | `array of strings` - Required        | What you want predicted for each cell type. Array needs to be the same length as `cell_types` or 1 value that is applied to all values in `cell_types`. "binding_fillHere" can be for any type of binding assay (ex. CHIP-Seq, H3k27ac) and the text trailing the "_" is not case sensitive  : ["accessibility", "binding_fillHere" , expression", "chromatin_confirmation"]                                                                                                                                                                                          | "prediction_types": ["expression", "binding_H3K4me3", "accessibility", "binding_CTCF"]                                                                                                                                          |
| `cell_types`        | `array of strings` - Required       | What cell type do you want for each `prediction_types`. Array needs to be the same length as `prediction_types` or only 1 value which will default for all `prediction_types`                                                                                                                                                                                | "cell_types" : ["HEPG2", "K562", "K562", "iPSC"]                                                                                                                                                                 |
| `scale`             | `array of strings` - Optional                 | How would you like the predictions scaled upon return (if at all). Array needs to be the same length as `prediction_types` : ["linear", "log"]                                                                                                                                                                                                                                                                         | "scale" : ["log", "log", "linear", "linear"]                                                                                                                                                                                           |
| `strand`            | `string`- Optional                  | Which strand would you like to be predicted  : ["positive", "negative"] ** we don't think this field is needed but have left it here for discussion                                                                                                                                                                                                                                                                                      | "strand": "positive"                                                                                                                                                                                     |
| `upstream_seq`      | `string`- Optional                  | Upstream flanking sequences to add to each sequence in `sequences`.                                                                                                                                                                                                                                                                                       | "upstream_seq" : "AATTA"                                                                                                                                                                                |
| `downstream_seq`    | `string`- Optional                  | Downstream flanking sequences to add to each sequence in `sequences`.                                                                                                                                                                                                                                                                                    | "downstream_seq" : "CCCAAAA"                                                                                                                                                                            |
| `sequences`         | `array of strings` - Required       | A collection of key-value pairs. Array of sequences with unique sequence id keys - any characters [A-Z][a-z][0-9][-.\_\~#\@%^&\*()]. The sequence id keys are matched to the predictor sequence id keys automatically by predictor. **allowing all of these characters is not necessary but we have left it here for discussion                                                                                                                             | "sequences" : [<br> {<br>   "seq1" : "ATGC...",<br>   "seq2" : "ATGC...",<br>  "random_seq" : "ATGC...",<br>  "enhancer" : "ATGC...",<br>  "control" : "ATGC..." <br> }<br>]                                   |
| `prediction_ranges` | `multi-dimensional array`- Optional | A collection of key-value pairs, where the keys should be identical to sequence id keys and values are multi/single-dimensional array based on what regions you want included in the predictions for each sequence. Sub-arrays of 2 integers mark the start and end location of the range of prediction you are interested in and you can have multiple starts and stops per sequence.| "prediction_ranges" : [<br>  {<br>   "seq1" : [0,1000] ,<br>   "seq2" : [100,110],<br>  "random_seq" : [ <br>    [0,10],<br>    [15,100] <br>   ],<br>  "enhancer" :    [210,500],<br>  "control" : [] <br> }<br>] |

Note: keys in `sequences` must be unique or will be overwritten during the reading in. 
### Predictor return message

| Key                | Value type - Required/Optional             | Description                                                                                                                                                                                                | Example Values                |
|---------------|---------------|-----------------------------|---------------|
| `task`             | `string`- Required           | What task was completed by the model: ["predict", "interpret", "help"]                                                                                                                                                                         | "task" : "predict"      |
| `prediction_types`  | `array of strings` - Required        | What was predicted for each cell type. Array needs to be the same length as `cell_types` or 1 value that is applied to all values in `cell_types`. "binding_fillIN" can be for any type of binding assay (ex. CHIP-Seq, H3k27ac) and the text trailing the "_" is not case sensitive  : ["accessibility", "binding_fillHere" , expression", "chromatin_confirmation"]                                                                                                                                                                                          | "prediction_types": ["expression", "binding", "accessibility", "binding_CTCF"]                                                                                                                                          |
| `scale_prediction` | `array of strings` - Optional            | How did the predictor scale the predictions (if at all): : ["linear", "log"] . Array needs to be the same length as `prediction_types`.                                                                                                                                                    | "scale" : ["log", "log", "linear", "linear"]          |
| `bin_size` | `integer` - Required            | Resolution of the model's predictions.                                                                                                                                                    | "bin_size" : 1          |
| `cell_types`       | `array of strings`- Required | Cell types used by the predictor for each of the `prediction_types` or one 1 cell type for all. Predictor can choose to use cell type/cell line ontology container which will returned the closest matched cell type that the predictor has.                                   | "cell_types" : ["HEPG2"] |
| `aggregation`      | `string`- Optional           | How replicate tracks were aggregated for each of the `prediction_types`. Array needs to be the same length as `prediction_types`.                                                                                                                                     | "aggregation" : ["mean", "mean", "mean"]   |
| `predictions`      | `Array of floats/integers/base64`- Required    | Objects of key-value pairs. The number of objects should be the same as the length of `prediction_types`. Each array of predictions can be a single value, a list of values for track predictions or a base64 string that encodes interaction matrices. The sequence ids are matched to the evaluator sequence ids automatically by predictor |"predictions" : [<br> {<br>   "seq1" :  [12.2, 5, 6, ..],<br>   "seq2" : [1.1, 12, 0.00, ..],<br>  "random_seq" : [100.1, 50, 0.5, ..],<br>  "enhancer" : [4, 3.0, 0.001, ..],<br>  "control" : [0, 0, 0, ..] <br> }<br>]<br>                         |

### Retrive information about predictor classes

Any evaluator can retrieve information from a predictor by asking for `help` in the `task` key. This will return a `.json` file that is written by the predictor, while these are not mandatory we highly encourage detailed `help` responses to organize and document predictor containers. 

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
| `features`              | `array of strings`- Optional   | List of features that the model predicts for each of the cells in `cell_types`.                                                 | "features" : ["accessibility", "accessibility", "binding_H3K4me3","binding_CTCF","expression", "expression", "expression"] |
| `cell_types`              | `array of strings`- Optional   | Cell types that correspond to predicted features in `features`.                                                 | "cell_types" : ["iPSC", "Hepg2", "iPSC", "iPSC", "iPSC", "HepG2",  "K562"] |
| `species`               | `array of strings`- Optional  | Name of species that the model predicts for.                                                   | "species" : ["yeast", "human"]|
| `author`                | `string`- Optional  | Paper author/authors or name of container builder                                                                  |  "author" : "Ishika Luthra" |
| `input_size`            | `Integer`- Optional | Number of base pairs of sequence that the model requires as input                                                  | "input_size" : 500500 |
| `output_size`           | `Integer`- Optional | Length of region that the model predicts across. Can also be one for single prediction models.                  | "output_size" : 100000|
| `bin_size`            | `Integer`- Optional | For models that predict across genomic tracks what is the base pair resolution                                     | "bin_size" : 10|
| `max_prediction_length` | `Integer`- Optional | What is the maximum sequence length you can provide before the model will no longer be able to handle the sequence | "max_prediction_length" : 2000000

### Error messages

Error messages that should be returned by the predictors in .json format. Error messages should be returned via one of the 3 possible keys so that the evaluators can "catch" the exception. Values can follow the format described below (any type) or other/additional ones can be added by the predictor builders.

We encourage predictor builders to return error messages in the format show below. Helper functions that have some basic error catching to build off can be found in the `src` folder. 

| Error Message Keys    | Value type |Description                                               | Example Values                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|-------------|-------------|----------------------------------------------|---------------------|
| `bad_prediction_request`    | `array of strings` |Request was unacceptable - model did not run          | •.json file is formatted incorrectly <br> •mandatory key `x` is missing in .json <br> •`task` requested is not recognized. Please choose from the following list `["predict", "interpret", "help"]` <br>• Value in `prediction_types` is not recognized. Please choose from the following list `["accessibility", "binding_fillHere" , expression", "chromatin_confirmation"]` <br> •duplicate sequence id key in `sequences`: sequence id key `y` is duplicated <br> •`prediction_ranges` are required to be integers <br> •length of `prediction_types` should be the same as length of `cell_types` or only 1 value <br> •sequence ids in `prediction_ranges` do not match those in `sequences` <br> •length of each sub-array in `prediction_ranges` should not be greater than 2 <br> • sequence id `z` has an invalid character present <br> |
| `prediction_request_failed` | `array of strings` |Evaluator message was valid -  model prediction was incomplete | • "seq_z" in `sequences` has an invalid character present <br> • model cannot handle sequence lengths this large <br>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `server_error`              | `array of strings` | Backend issue                                             | •socket communication failed <br> •wifi error <br> •memory error (eg. due to large batch size, due to large .json file)                                                                                                                                                                                                                                                                                                                                                                                                                                                  
### Containerizing evaluators and predictors

TO DO: add information here about how to create singularity containers

