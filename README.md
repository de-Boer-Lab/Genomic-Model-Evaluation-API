---
---
---

# Genomic Model Evaluation API

### API Reference

This Application Programming Interface (API) was designed for the functional genomics community to create seamless communication across pre-trained models and genomics datasets. It is a product of the feedback from many model and dataset experts and our hope is that it allows for long-lasting benchmarking of models. Models and datasets communicate via a set of predefined protocols through APIs. The common protocol enables any model to communicate with any dataset (although not all combinations may make sense).

The evaluators (dataset APIs) will make prediction requests in the standard format (seen below) to the predictors (model APIs), which then return the predictions to the Evaluator in a standard format, enabling the evaluators to calculate the model’s performance. Each of the evaluators and predictors will be containerized using Singularity (more details below).

The communication protocol below covers some of the mandatory parameters required for the API. There are also some optional parameters for specific prediction requests. 

For this effort to succeed we encourage data and model experts to provide us with feedback and support (via contributing evalutors and predictors). Since dataset creators are the experts in their dataset, they are most qualified to decide how these models should be evaluated on their data. Meanwhile, model creators are best qualified for deciding how the model should be used for the inference tasks. Accordingly, the responsibilities for adding the new datasets and models would fall on their creators. Once they set up the intial Being able to easily compare results across different datasets and models would accelerate the improvement of genomics models, motivate novel functional genomic benchmarks, and provide a more nuanced understanding of model abilities.

If you would like to be involved we encourage you to use this API with your own models and datasets and submit to the Github repo list (add link). If you have critiques or feedback please reach out to [ishika.luthra\@ubc.ca](mailto:ishika.luthra@ubc.ca). The protocol is still under development, **indicates specific ideas we would like feedback on. 

![](./src/API_V2.png)

### Communication protocol

Using the standardized communication format each Predictor will receive information in the same format from any evalutor. Each Predictor also returns the predictions in the same format which enables the community to easily compare different model's predictions for the same dataset or evaluate a model on multiple different types of datasets very quickly. 

The only files that are exchanged between the evaluators and predictors are .json files, a commonly used file format for sending and receiving information in a standard format. Data in the .json files is stored in the following format: `"keys": "value"`, where the value can be strings, numbers, objects, arrays, booleans or null. We have outlined below the mandatory "keys" required for communication between the Evaluator and Predictor to occur. Certain "keys" have a fixed set of "values" that can be used while others are up to the evaluators.

The files and communication between APIs is done using python sockets. Scripts for these can be found in `\src\socket_scripts\`.

Examples of Evaluator and Predictor messages can be found in `\examples\json\` folder. Formats for json files can be checked using the following link: https://jsonformatter.curiousconcept.com

Examples of containerized evaluators and predictors can be found in `\examples\containers\` folder. 

#### Communication protocol example

P: Hi my name is "Predictor"! My job is to wait and listen for a "Evaluator" to ask me to do something.

E: Hello I'm an "Evaluator"! I'm sending you a .json file, could you please predict the accessbility of these sequences?

P: Sure thing :) One moment please...

P: Psst! Hey CellMatcher! I was asked for cellX, but I have no clue that that is, can I have a little help?

CM: Sure thing! cellX is similar to your cellY, so you should use that for your predictions instead. 

P: Here you go, Evaluator - i'm sending you a .json file back with all the predictions for cellY.
                      
### An example for how issue a request from the Predictor

The example below outlines an easy test communication between an Evaluator (with random sequences) and a Predictor (that will generate random predictions for any task you request). 

TO ADD

`python`

### Evaluator request message

| Key                 | Value type - Required/Optional                   | Description: Value options                                                                                                                                                                                                                                                                                                                                                  | Example                                                                                                                                                                                                 |
|--------------|--------------|-------------------------------|--------------|
| `request`              | `string` - Required                 | Requested task for Predictor : ["predict", "help"].                                                                                                                                                                                                                                                                         | "request": "predict"                                                                                                                                                                                       |
| `readout`           | `string` - Required                | Type of readout that is requested from the Predictor: ["point","track", "interaction_matrix"].                                                                                                                                                                                                                                                                              | "readout": "track"                                                                                                                                                                                      |
| `prediction_task`  | `array of objects` - Required        | Each object must contain the following keys: `name`, `type`, `cell_type`, `species`, `scale`(optional).                                                                                                                                                                                          | "prediction_task": [<br> {<br>   "name": "task1",<br>   "type": "expression",<br>  "cell_type": "iPSC",<br>  "scale": "linear",<br>  "species": "homo_sapiens" <br> }<br>]                                                                                                                                          |
| `name`  | `string` - Required        | Unique identifier for each prediction task array.                                                                                                                                                                                          | "name": "model_prediction"                                                                                                                                          |
| `type`  | `string` - Required        | Prediction type you want predicted. "binding_<molecule>" can be for any type of binding assay (ex. CHIP-Seq, H3k27ac) and the text trailing the "_" is not case sensitive  : ["accessibility", "binding_molecule" , expression", "chromatin_confirmation"].                                                                                                                                                                                          | "type": "expression"                                                                                                                                         |
| `cell_type`        | `string` - Required       | What cell type you want predicted for `type`.                                                                                                                                                                                | "cell_type": "K562"                                                                                                                                                            |
| `species`        | `string` - Required       | What species you want predicted for `type`.                                                                                                                                                                              | "species": "homo_sapiens"                                                                                                                                                                |
| `scale`             | `string` - Optional                 | How would you like the predictions scaled upon return (if at all): ["linear", "log"].                                                                                                                                                                                                                                                                         | "scale" : "linear"                                                                                                                                                                                         |
| `upstream_seq`      | `string`- Optional                  | Upstream flanking sequences to add to each sequence in `sequences`.                                                                                                                                                                                                                                                                                       | "upstream_seq": "AATTA"                                                                                                                                                                                |
| `downstream_seq`    | `string`- Optional                  | Downstream flanking sequences to add to each sequence in `sequences`.                                                                                                                                                                                                                                                                                    | "downstream_seq": "CCCAAAA"                                                                                                                                                                            |
| `sequences`         | `object` - Required       | A collection of key-value pairs (strings). Keys are unique sequence ID keys - any characters [A-Z][a-z][0-9][-.\_\~#\@%^&\*()].* The sequence ID keys are matched to the Predictor sequence ID keys automatically by Predictor.**                                                                                                                             | "sequences": {<br>   "seq1": "ATGC...",<br>   "seq2": "ATGC...",<br>  "random_seq": "ATGC...",<br>  "enhancer": "ATGC...",<br>  "control": "ATGC..." <br> }                                  |
| `prediction_ranges` | `object` - Optional | A collection of key-value pairs, where the keys should be identical to sequence ID keys and values are arrays with the start and end region you want predicted for each sequence. Start and end are 0 indexed and inclusive (e.g. [0,1] is the first two bases)***.| "prediction_ranges": {<br>   "seq1": [0,1000] ,<br>   "seq2": [100,110],<br>  "random_seq": [],<br>  "enhancer": [210,500],<br>  "control": [] <br> } |

*keys in `sequences` must be unique or will be overwritten during the reading in. 
**all indexing is 0 based 
***to minimize any bias from the predictors we suggested randomizing your sequences so that there is no dependency on the order

### Predictor return message

| Key   | Value type - Required/Optional             | Description                                                                                                                                          | Example Values                |
|-----|---------------|-----------------------------|-----------------------------|
| `request` | `string`- Required           | What request was completed by the model: ["predict", "help"]                                                                                                                                                                         | "task": "predict"      |
| `bin_size` | `integer` - Required for track based models           | Resolution of the model's predictions.                                                                                                                                                    | "bin_size" : 1          |
| `prediction_task`  | `array of objects` - Required        | Each object must contain the following keys: `name`, `type_requested`,`type_actual`, `cell_type_requested`, `cell_type_actual`, `species_requested`, `species_actual`, `scale_prediction_requested` (optional), `scale_prediction_actual` (optional), `aggregation_replicates` (optional).                                                                                                                                                                                          | "prediction_task": [<br> {<br>   "name": "task1",<br>   "type_requested": "expression",<br>  "type_actual": "expression",<br>  "cell_type_requested": "K562",<br>  "cell_type_actual": "bone_marrow_cell_line",<br>  "species_requested": "homo_sapiens",<br>  "species_actual": "homo_sapeins",<br>  "scale_prediction_requested": "linear", <br>  "scale_prediction_actual": "linear",<br>  "aggregation_replicates": "mean",<br>   "predictions": { <br>     "seq1": [12.2, 5, 6, ..],<br>     "seq2": [1.1, 12, 0.00, ..],<br>    "random_seq": [100.1, 50, 0.5, ..],<br>    "enhancer": [4, 3.0, 0.001, ..],<br>    "control": [0, 0, 0, ..] <br>   }<br> }<br>]                                                                                                                                          | `name`  | `string` - Required        | Unique identifier for each prediction task array matched from Evaluator.|
| `type_requested`  | `string` - Required        | Prediction type requested. "binding_<molecule>" can be for any type of binding assay (ex. CHIP-Seq, H3k27ac) and the text trailing the "_" is not case sensitive: ["accessibility", "binding_molecule" , expression", "chromatin_confirmation"].                                                                                                                                                                                          | "type_requested": "expression"                                                                                                                                         |
| `type_actual`  | `string` - Required        | Prediction type compleated by Predictor.                                                                                                                                                                                          | "type_actual": "expression"                                                                                                                                   | `cell_type_requested`       | `string`- Required | Cell type requested by Predictor.                                   | "cell_type_requested": ["HEPG2"] |
  | `cell_type_actual`       | `string`- Required | Cell type returned by Predictor. Predictor can choose to use cell type/cell line ontology container which will returned the closest matched cell type that the Predictor has.                                   | "cell_type_actual": ["HEPG2"] |
  | `species_requested`        | `string` - Required       | What species was requested by the Predictor.                                                                                                                                                                              | "species_requested": "homo_sapiens"                                                                                                                                                                | `species_actual`        | `string` - Required       | What species was used by the Predictor.                                                                                                                                                                              | "species_actual": "homo_sapiens"                                                                                                                                                                |
| `scale_prediction_requested` | `string` - Optional            | Evaluator requested scaling for predictions: ["linear", "log"].                                                                                                                                                    | "scale_prediction_requested": "log"       |
| `scale_prediction_actual` | `string` - Optional            | How did the Predictor scale the predictions (if at all): ["linear", "log"] .                                                                                                                                                   | "scale_prediction_actual": "log"    | `aggregation_replicates`      | `string`- Optional           | How replicate tracks were aggregated for each of the `prediction_types`. Array needs to be the same length as `prediction_types`.                                                                                                                                     | "aggregation": ["mean", "mean", "mean"]   |
| `predictions`      | `object`- Required    | Objects of key-value pairs where keys are strings and values are arrays of floats/integers/base64. Each array of predictions can be a single value, a list of values for track predictions or a base64 string that encodes interaction matrices. The sequence ID keys are matched to the Evaluator sequence ID keys automatically by Predictor |"predictions": {<br>   "seq1": [12.2, 5, 6, ..],<br>   "seq2": [1.1, 12, 0.00, ..],<br>  "random_seq": [100.1, 50, 0.5, ..],<br>  "enhancer": [4, 3.0, 0.001, ..],<br>  "control": [0, 0, 0, ..] <br> }                         |

### Retrive information about Predictor classes

Any Evaluator can retrieve information from a Predictor by asking for `help` in the `task` key. This will return a `.json` file that is written by the Predictor, while these are not mandatory we highly encourage detailed `help` responses to organize and document Predictor containers. 

Message sent by evalutor:

| Key: Value    | Value type- Required/Optional  |Description                                                                 |
|--------------|--------------|---------------------|
| "task": "help" | `string`- Required| Retrieve basis information about the Predictor (written by model developers) |

Message returned by Predictor:

| Key  | Value type     | Description       | Example Values |
|------|---------------|-------------------------------------------|-------------------|
| `model`                 | `string`- Optional  | Model name.                                                                                                         | "model": "deBoer Lab test" |
| `version`               | `string`- Optional  | Information about version of Predictor.                                                                                 | "version": "2.2"|
| `publication`               | `string`- Optional  | Citation for original paper.                                                                                | "publication": "Luthra et. al, 2024"|
| `build_date`            | `string`- Optional  | Date the Predictor container was built - to track potential rebuilds.                                               | "build_date": "Aug 20, 2024"|
| `features`              | `array of strings`- Optional   | List of features that the model predicts for each of the cells in `cell_types`.                                                 | "features": ["accessibility", "accessibility", "binding_H3K4me3","binding_CTCF","expression", "expression", "expression"] |
| `cell_types`              | `array of strings`- Optional   | Cell types that correspond to predicted features in `features`. Length of "cell_types" should be the same as "features" or length 1.                                              | "cell_types": ["iPSC", "Hepg2", "iPSC", "iPSC", "iPSC", "HepG2",  "K562"] |
| `species`               | `array of strings`- Optional  | Species that correspond to predicted features in `features`. Length of "species" should be the same as "features" or length 1.                                               | "species": ["homo_sapiens"]|
| `container_authors`                | `string`- Optional  | Author/authors of container builders.                                                                 |  "container_authors": "Ishika Luthra" |
| `model_authors`                | `string`- Optional  | Paper author/authors.                                                                  |  "model_authors": "Ishika Luthra" |
| `input_size`            | `Integer`- Optional | Number of base pairs of sequence that the model takes as input.                                                  | "input_size" : 500500 |
| `bin_size`            | `Integer`- Optional | For models that predict across genomic tracks what is the base pair resolution.                                     | "bin_size": 10|
| `expression_strand_specific` | `Boolean`- Optional | For models that predict expression, is the expression prediction strand specific or not. | "expression_strand_specific": true|
### Error messages

Error messages that should be returned by the predictors in .json format. Error messages should be returned via one of the 3 possible keys so that the evaluators can "catch" the exception. Values can follow the format described below (any type) or other/additional ones can be added by the Predictor builders.

We encourage Predictor builders to return error messages in the format show below. Helper functions that have some basic error catching to build off can be found in the `src` folder. 

| Error Message Keys    | Value type |Description                                               | Example Values                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|-------------|-------------|----------------------------------------------|---------------------|
| `bad_prediction_request`    | `array of strings` |Request was unacceptable - model did not run.          | •.json file is formatted incorrectly. <br> •Mandatory key `x` is missing in .json. <br> •`request` value is not recognized. Model developers can choose what to return here. <br>•Value in `type` is not recognized. Model developers can choose what to return here. <br> •Duplicate sequence ID key in `sequences`: sequence ID key `y` is duplicated. <br> •`prediction_ranges` are required to be integers. <br> •Sequence ids in `prediction_ranges` do not match those in `sequences`. <br> •Length of each sub-array in `prediction_ranges` should not be greater than 2. <br> •Sequence ID key `z` has an invalid character present. <br> |
| `prediction_request_failed` | `array of strings` |Evaluator message was valid -  model prediction was incomplete. | •"seq_z" in `sequences` has an invalid character present. <br> •Model cannot handle sequence lengths this large. <br>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `server_error`              | `array of strings` | Backend issue.     | •Socket communication failed. <br> •Wifi error. <br> •Memory error (eg. due to large batch size, due to large .json file).                                                                                                                                                                                                                                                                                                                                                                                                                                                 
### Containerizing evaluators and predictors

TO DO: add information here about how to create singularity containers


### Collaborators

* Sara Mostafavi
  + Xinming Tu
  + Yilun Sheng
* Anshul Kundaje
  + Surag Nair
  + Soumya Kundu
  + Ivy Raine
  + Vivian Hecht
* Brenden Frey
  + Alice Gao
  + Phil Fradkin
* Graham McVicker
  + Jeff Jaureguy
  + David Laub
  + Brad Balderson
  + Kohan Lee
  + Ethan Armand
* Hannah Carter
  + Adam Klie
* Maxwell Libbrecht
* Ivan Kulakovskiy
  + Dima Penzar
  + Ilya Vorontsov
* Vikram Agarwal
* Peter Koo
* Ziga Avsec
* Jay Shendure
  + CX Qiu
  + Diego Calderon
* Julien Gagneur
  + Thomas Mauermeier
* Sager Gosai
* Andreas Gschwind
* Ryan Tewhey
* David Kelley
* Georg Seelig
* Gokcen Eraslan
* Jesse Engreitz
* Jian Zhou
* Julia Zeitlinger
* Kaur Alosoo
* Luca Pinello
* Michael White
* Rhiju Das
* Stein Aerts

