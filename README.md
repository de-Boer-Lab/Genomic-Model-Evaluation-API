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

`OK` communication was successful

`bad prediction request` Request was unacceptable. Could be due to evalutor message format (.json is not formatted correctly, or a mandatory paramter is missing)

`prediction request failed` The parameters were valid but request for prediction was not successful. 

`number of sequences do not match number of prediction ranges` Each sequence must be given a range on which to predict, can also be left empty

`duplicate sequence names` Each sequence id requires a unique identifier 

`prediction_task not found` prediction task key is incorrect

`server error` Something went wrong on on the backend (could be due to socket error or wifi error)

### Evaluator request metadata

`"prediction_task": task that is being asked of the predictor`

`"type": what do you want predicted`

`"cell_type": what is the evalutor cell types/cell types`

`"tracks": what tracks would you like returned`

`"scale": what scale would you like the predictors returned in`

`"upstream_seq": flanking sequences to add to each evaluator sequence upstream`

`"downstream_seq": flanking sequences to add to each evaluator sequence downstream`

`"sequences": array of unique sequence ids (can be anything) with the correspond sequences` 

`"prediction_ranges": for models that predict across a track what range would you like the prediction across. This can also be left blank`

### Prediction return metadata


`"prediction_task": what task was compleated by the model`

`"scale_prediction": how does the predictor scale the predictions`

`"cell_type": what cell type was used from the predictor`

`"tracks": what were the tracks used from the predictor`

`"aggregation": how were replicate tracks aggregated`
  
`"predictions": array of predictions can be a single value or list of values for track predictions. The sequence ids are matched to the evaluator sequence ids`

### Retrive information about predictor classes

Any evaluator can retrieve information from a predictor by asking for "help" in the "prediction_task" key. This will return a `.json` file that is written by predictor builders. The keys attached below are mandatory for the communication 

Message sent by evalutor:

`"prediction_task": "help"`

Message returned by predictor: 

`"model": insert model name here`

`"version": model version to track model updates by authors`

`"build_date": date the predictor container was built`

`"features": array of model cell types and corresponding tracks`

`"species" training species`

`"author": author/authors names`

`"input_size": input window lenght of model`

`"output_size": size of model prediction`

`"resolution": prediction resolution`

