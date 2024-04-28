---
---
---

# Genomic Model Evaluation API

### API Reference

Our Application Programming Interface (API)-type approach allows for seamless communication across pre-trained models and functional genomics datasets on which those models can be benchmarked. Models and datasets will communicate via a set of predefined protocols through APIs. The common protocol will enable any model to communicate with any dataset (although not all combinations may make sense).

The evaluators will make prediction requests in the standard format (seen below) to the predictors, which then return the predictions to the dataset client in a standard format, enabling the evaluators to calculate the model’s performance.

The communication protocol below covers the mandatory parameters required for the API but users are able to add more parameters/functions.

For our efforts to succeed we require community support and feedback from data and models experts so that the design will result in a stable long-term solution for model benchmarking. Since dataset creators are the experts in their dataset, they are most qualified to decide how these models should be evaluated on their data. Meanwhile, model creators are best qualified for deciding how the model should be used for the inference tasks. Accordingly, the responsibilities for adding the new datasets and models would fall on their creators. Being able to easily compare results across different datasets and models would accelerate the improvement of genomics models, motivate novel functional genomic benchmarks, and provide a more nuanced understanding of model abilities.

If you would like to be involved we encourage you to use this communication protocol with your own models and datasets and submit to the Github repo list (add link). If you have critiques or feedback please reach out to [ishika.luthra\@ubc.ca](mailto:ishika.luthra@ubc.ca)

![](./src/API_V2.png)

Example of containers for evalutors, predictors and scripts for communication can be found in the `examples` folder.

### Error messages

Error messages that can be returned by the predictors:

We encourage predictor

| Error Message Categories    | Description                                               | Type                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|-------------|-------------|----------------------------------------------|
| `bad prediction request`    | Request was unacceptable - Predictor did not run          | •.json file is formatted incorrectly <br> •mandatory key `x` is missing in .json <br> •`task` requested does not exist. Please choose from the following list `["predict", "interpret", "help"]` <br> •duplicate sequence ids in `sequences`: sequence id `y` is duplicated <br> •`prediction_ranges` are required to be integers <br> •length of `prediction_types` should be the same as length of `cell_types` or only 1 value <br> •sequence ids in `prediction_ranges` do not match those in `sequences` <br> •length of each sub-array in `prediction_ranges` should not be greater than 2 <br> |
| `prediction request failed` | Evaluator message was valid but prediction was incomplete | • sequence id `z` has an invalid character present <br> • predictor cannot handle sequence lengths this large <br>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `server error`              | Backend issue                                             | •socket communication failed <br> •wifi error <br> •memory error due to large batch size <br> •memory error due to large .json file                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |

### Evaluator request message

| Key                 | Value                     | Description                                                                                                                                                                                                                                                                                                                                                  | Example                                                                                                                                                                                                 |
|--------------|--------------|-------------------------------|--------------|
| `task`              | `string`                  | What task you are asking the predictor to complete: ["predict", "interpret", "help"]                                                                                                                                                                                                                                                                         | "task": "predict"                                                                                                                                                                                       |
| `readout`           | `string`                  | What is the readout from the predictor: ["point","track", "interaction_matrix"]                                                                                                                                                                                                                                                                              | "readout": "track"                                                                                                                                                                                      |
| `prediction_types`  | `array of strings`        | What you want predicted for each cell type. Array needs to be the same length as `cell_types`: ["accessibility", "binding" , expression", "chromatin_confirmation"]                                                                                                                                                                                          | "prediction_types": ["expression", "accessibility", "binding"]                                                                                                                                          |
| `cell_types`        | `array of strings`        | What cell type do you want for each `prediction_types`. Array needs to be the same length as `prediction_types` or only 1 value which will default for all `prediction_types`                                                                                                                                                                                | "cell_types": ["HEPG2", "K562", "K562"]                                                                                                                                                                 |
| `scale`             | `string`                  | How would you like the predictors scaled upon return (if at all) : ["linear", "log"]                                                                                                                                                                                                                                                                         | "scale":"log"                                                                                                                                                                                           |
| `strand`            | `string`                  | Which strand would you like to be predicted : ["positive", "negative"]                                                                                                                                                                                                                                                                                       | "strand":"positive"                                                                                                                                                                                     |
| `upstream_seq`      | `string`                  | Upstream flanking sequences to add to each sequence. Can be left blank.                                                                                                                                                                                                                                                                                      | "upstream_seq" : "AATTA"                                                                                                                                                                                |
| `downstream_seq`    | `string`                  | Downstream flanking sequences to add to each sequence. Can be left blank.                                                                                                                                                                                                                                                                                    | "downstream_seq" : "CCCAAAA"                                                                                                                                                                            |
| `sequences`         | `array of strings`        | A collection of key-value pairs. Array of sequences with unique sequence ids - any characters [A-Z][a-z][0-9][-.\_\~#\@%^&\*()]. The sequence ids are matched to the predictor returned sequence ids automatically by predictor                                                                                                                              | "sequences":[<br> {<br>   "seq1": "ATGC...",<br>   "seq2": "ATGC...",<br>  "random_seq": "ATGC...",<br>  "enhancer": "ATGC...",<br>  "control": "ATGC..." <br> }<br>]                                   |
| `prediction_ranges` | `multi-dimensional array` | A collection of key-value pairs, where the value is a multi/single-dimensional array based on what regions you want included in the predictions for each sequence. Sub-arrays of 2 integers mark the start and end location of the range of prediction you are interested in. The keys should be identical to the sequence ids. This can also be left blank. | "prediction_ranges":[<br>  {<br>   "seq1": [0,1000] ,<br>   "seq2": [100,110],<br>  "random_seq":[ <br>    [0,10],<br>    [15,100] <br>   ],<br>  "enhancer":    [210,500],<br>  "control": [] <br> }<br>] |

### Predictor return message

| Key                | Value              | Description                                                                                                                                                                                                | Example                 |
|---------------|---------------|-----------------------------|---------------|
| `task`             | `string`           | What task was completed by the model                                                                                                                                                                       | "task" : "predict"      |
| `scale_prediction` | `string`           | How did the predictor scale the predictions (if at all)                                                                                                                                                    | "scale": "log"          |
| `cell_types`       | `array of strings` | Cell types used by the predictor for each of the `prediction_types` or one 1 cell type for all. Returned from closest match from cell type/cell line ontology container.                                   | "cell_types": ["HEPG2"] |
| `aggregation`      | `string`           | How replicate tracks were aggregated for each of the `prediction_types`                                                                                                                                    | "aggregation": "mean"   |
| `predictions`      | `Array of floats/integers`    | A collection of key-value pairs. Array of predictions can be a single value or list of values for track predictions. The sequence ids are matched to the evaluator sequence ids automatically by predictor |"predictions":[<br> {<br>   "seq1": [12.2, 5, 6, ..],<br>   "seq2": [1.1, 12, 0.00, ..],<br>  "random_seq": [100.1, 50, 0.5, ..],<br>  "enhancer": [4, 3.0, 0.001, ..],<br>  "control": [0, 0, 0, ..] <br> }<br>                         |

### Retrive information about predictor classes

Any evaluator can retrieve information from a predictor by asking for `help` in the `task` key. This will return a `.json` file that is written by predictor builders. The keys attached below are mandatory for the communication

Message sent by evalutor:

| Key    | Value  | Description                                                                 |
|--------------|--------------|--------------------------------------------|
| `task` | `string` | Retrieve basis information about the predictor (written by model developers) |

Message returned by predictor:

| Key                     | Value     | Description       | Example |
|---------------|---------------|-------------------------------------------|----------|
| `model`                 | `string`  | Model name                                                                                                         | "model":Enformer" |
| `version`               | `string`  | Information about version of model                                                                                 | "version": "2.2"|
| `build_date`            | `string`  | Date the predictor container was built - to track potential rebuilds                                               | "build_date": "Aug 20, 2024"|
| `features`              | `multi dimensional array`   | List of features that the model predicts and for which cell types.                                                 | "features": [<br> {<br>   "HEPG2": ["DNase", "H3K4me3",...],<br>   "iPSC": ["H3K4me3", "DNase",...],<br>  "Adult liver": ["CAGE", "DNase",...]] |
| `species`               | `array of strings`  | Name of species that the model predicts for - can be more than 1                                                   | "species": ["mouse", "human"]|
| `author`                | `string`  | Paper author/authors or name of container builder                                                                  |  "author": "David R. Kelley" |
| `input_size`            | `Integer` | Number of base pairs of sequence that the model requires as input                                                  | "input_size": 393,639 |
| `output_size`           | `Integer` | Number of base pairs that the models predicts across. Can also be 0 for single prediction models.                  | "output_size": 114,688|
| `resolution`            | `Integer` | For models that predict across genomic tracks what is the base pair resolution                                     | "resolution": 128|
| `max_prediction_length` | `Integer` | What is the maximum sequence length you can provide before the model will no longer be able to handle the sequence | "max_prediction_length": "2MB"
