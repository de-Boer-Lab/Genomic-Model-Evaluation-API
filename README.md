# Genomic Model Evaluation API 

### API Reference

Our Application Programming Interface (API)-type approach allows for seamless communication across pre-trained models and functional genomics datasets on which those models can be benchmarked. Models and datasets will communicate via a set of predefined protocols through APIs. The common protocol will enable any model to communicate with any dataset (although not all combinations may make sense). 

The evaluators will make prediction requests in the standard format (seen below) to the predictors, which then return the predictions to the dataset client in a standard format, enabling the evaluators to calculate the model’s performance.

The communication protocol below covers the mandatory parameters required for the API but users are able to add more parameters/functions.

For our efforts to succeed we require community support and feedback from data and models experts so that the design will result in a stable long-term solution for model benchmarking. Since dataset creators are the experts in their dataset, they are most qualified to decide how these models should be evaluated on their data. Meanwhile, model creators are best qualified for deciding how the model should be used for the inference tasks. Accordingly, the responsibilities for adding the new datasets and models would fall on their creators. Being able to easily compare results across different datasets and models would accelerate the improvement of genomics models, motivate novel functional genomic benchmarks, and provide a more nuanced understanding of model abilities.

If you would like to be involved we encourage you to use this communication protocol with your own models and datasets and submit to the Github repo list (add link). If you have critiques or feedback please reach out to ishika.luthra@ubc.ca

![](./src/API_V2.png)

Example of containers for evalutors, predictors and scripts for communication can be found in the `examples` folder.

### Error messages

Error messages that can be returned by the predictors:


| Error Message Categories    | Description                     | Type                      |
|-----------------------------|---------------------------------|---------------------------|
| `bad prediction request`     | Request was unacceptable |•.json file is formatted incorrectly <br> •mandatory key is missing in .json <br> •`task` requested does not exist|
| `prediction request failed`      | Evaluator message was valid but prediction was not successful  |•duplicate sequence ids in `sequences` <br> •`prediction_ranges` are required to be integers <br> •length of `prediction_types` should be the same as length of `cell_types` <br> •sequence ids in `prediction_ranges` do not match those in `sequences` <br> •length of each value in `prediction_ranges` should not be greater than 2 <br>|
| `server error`     | Backend issue |•socket communication failed <br> •wifi error <br> •memory error due to large batch size <br>|


### Evaluator request message


| Key        | Value         | Description           |
|------------|---------------|--------------------|
| `task`     | `string` | What task you are asking the predictor to compleate: ["predict", "interpret", "help"] |
| `readout`     | `string` | What is the readout from the predictor: ["track", "point", "interaction_matrix"] |
| `prediction_types`     | `array of strings` | What you want predicted for each cell type. Array needs to be the same length as `cell_types`: ["expression", "accessibility", "expression", ...] |
| `cell_types`     | `array of strings` | What cell type do you want for each `prediction_types`. Array needs to be the same length as `prediction_types`: ["HEPG2", "K562", "K562",... ] |
| `scale`      | `string`  | How would you like the predictors scaled upon return (if at all)|
| `upstream_seq`     | `string` | Flanking sequences to add to each evaluator sequence upstream|
| `downstream_seq`     | `string` | Flanking sequences to add to each evaluator sequence downstream|
| `sequences`     | `array of strings` | A collection of key-value pairs. Array of sequences with unique sequence ids (can be anything). The sequence ids are matched to the predictor returned sequence ids automatically by predictor |
| `prediction_ranges`     | `array of 2 integers` | A collection of key-value pairs. Array of 2 integers that mark the start and end location of the range of prediction you are interested in. The keys should be identical to the sequence ids. This can also be left blank.

### Predictor return message


| Key        | Value         | Description           |
|------------|---------------|--------------------|
| `task`     | `string` | What task was completed by the model |
| `scale_prediction`      | `string`  | How did the predictor scale the predictions (if at all)|
| `cell_types`     | `array of strings` | Cell types used by the predictor for each of the `prediction_types`. Returned from closest match from cell type/cell line ontology container|
| `aggregation`     | `string` | How replicate tracks were aggregated for each of the `prediction_types`|
| `predictions`     | `Float/Integer` |A collection of key-value pairs. Array of predictions can be a single value or list of values for track predictions. The sequence ids are matched to the evaluator sequence ids automatically by predictor |


### Retrive information about predictor classes

Any evaluator can retrieve information from a predictor by asking for `help` in the `task` key. This will return a `.json` file that is written by predictor builders. The keys attached below are mandatory for the communication 

Message sent by evalutor:


| Key     | Value    | Description|
|---------|----------|------------|
| `task` | `help`                | Retrieve basis information about the predictor (written by model developers|


Message returned by predictor: 


| Key        | Value         | Description           |
|------------|---------------|--------------------|
| `model`     | `string` | Model name |
| `version`      | `string`  | Information about version of model|
| `build_date`     | `string` | Date the predictor container was built - to track potential rebuilds|
| `features`     | `array` | List of features that the model predicts and for which cell types. |
| `species`     | `string` |Name of species that the model predicts for - can be more than 1 |
| `author`     | `string` |Paper author/authors or name of container builder |
| `input_size`     | `Integer` | Number of base pairs of sequence that the model requires as input |
| `output_size`     | `Integer` |Number of base pairs that the models predicts across. Can also be 0 for single prediction models. |
| `resolution`     | `Integer` |For models that predict across genomic tracks what is the base pair resolution |
