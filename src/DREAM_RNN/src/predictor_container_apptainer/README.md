# Configuring Definition File and Running Predictor Container for Dream-RNN

## Overview

This container for Predictor includes:
    - Predictor script for sequence processing and error handling.
    - Integrated Dream-RNN model with its dependencies and DREAM conda environment created using `dreamRNN_environment.yml`.
    - Pre-trained model weights (`model_best.pth`) for predictions.
    - Support scripts like `api_preprocessing_utils.py`, `error_message_functions_updated.py`, and `predictor_help_message.json`.

## **Usage:**

We encourage using pre-built containers for this model that are hosted on Zenodo: https://zenodo.org/records/14649126.

However, if you are building the container using this definition file, ensure you have the following directory structure on the host:

```
/path/to/DREAM_RNN/src/predictor_container_apptainer/
├── predictor.def
├── predictor.sif
├── dreamRNN_API_script
│   ├── data
│   │   ├── evaluator_input_sample_test.json
│   │   ├── evaluator_message_more_complex.json
│   │   └── evaluator_message_simple_test.json
│   ├── dreamRNN_predict.py
│   ├── dream_rnn_k562_model_weight
│   │   └── model_best.pth
│   └── prixfixe
├── script_and_utils
│   ├── api_preprocessing_utils.py
│   ├── error_message_functions_updated.py
│   ├── predictor_API_clean_apptainer.py
│   └── predictor_help_message.json
```

### Build the container (SIF)

```bash
apptainer build predictor.sif predictor.def
```

### Run the container

```bash
apptainer run predictor.sif HOST PORT
```

## **Details:**

- The container receives data via a TCP socket and doesn’t require mounted data directories.
- Replace `HOST` and `PORT` with the server and port configuration for the evaluator.

## **Purpose:**

- Facilitates genomic model evaluation and prediction using the DREAM-RNN framework.
- It is designed to seamlessly integrate with other tools via API endpoints.

## **Example Command:**

```bash
apptainer run predictor.sif 172.16.47.244 5000
```

## **Arguments:**

1. `HOST`: IP address or hostname of the Predictor server.
2. `PORT`: Port number the Predictor is listening on.
