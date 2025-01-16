# Configuring Definition File and Running Evaluator Container for Dream-RNN

## Overview

This container includes:
    - Evaluator API script for genomic sequence evaluation.
    - Installed Python dependencies required by the Evaluator.

## **Usage:**

We encourage using pre-built containers for this model that are hosted on Zenodo: https://zenodo.org/records/14649126.

However, if you are building the container using this definition file, ensure you have the following directory structure on the host:

```
/path/to/DREAM_RNN/src/evaluator_container_apptainer/
├── evaluator.def
├── evaluator.sif
├── evaluator_API_clean_apptainer.py
├── evaluator_data
│   ├── evaluator_input_sample_test.json
│   ├── evaluator_message_more_complex.json
│   └── evaluator_message_simple_test.json
└── predictions
```

### Build the container (SIF)

```bash
apptainer build evaluator.sif evaluator.def
```

### Bind these directories and run the container

```bash
apptainer run \
    -B /path/to/DREAM_RNN/src/evaluator_container_apptainer/evaluator_data:/evaluator_data \
    -B /path/to/DREAM_RNN/src/evaluator_container_apptainer/predictions:/predictions \
    evaluator.sif PREDICTOR_HOST PREDICTOR_PORT /predictions
```

## **Details:**

- The container sends and receives data via a TCP socket and requires `/evaluator_data` and `/predictions` to be mounted at runtime.

## **Purpose:**

- Facilitates genomic sequence evaluation by interacting with the Predictor container.
- Handles input/output through bound directories.

## **Example Command:**

```bash
apptainer run \
    -B /path/to/DREAM_RNN/src/evaluator_container_apptainer/evaluator_data:/evaluator_data \
    -B /path/to/DREAM_RNN/src/evaluator_container_apptainer/predictions:/predictions \
    evaluator.sif 172.16.47.244 5000 /predictions
```

## **Arguments:**

1. `PREDICTOR_HOST`: IP address or hostname of the Predictor server.
2. `PREDICTOR_PORT`: Port number the Predictor is listening on.
3. `/predictions`: Path inside the container for storing output predictions.
