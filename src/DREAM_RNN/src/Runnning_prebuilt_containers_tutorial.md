# Running the DREAM-RNN container with a sample dataset

To run a test prediction using the DREAM-RNN container and sample Evaluator container:

1. Download the container from Zenodo: https://zenodo.org/records/14649126

```bash
mkdir DREAMRNN
mkdir test_evaluator
```

```bash
cd DREAMRNN
wget https://zenodo.org/records/14649126/files/predictor.sif?download=1
```

``` bash
cd test_evaluator
wget https://zenodo.org/records/14649126/files/evaluator.sif?download=1
wget eval
mkdir predictions
```


2. Get the IP Address of where the Predictor is running

Note: PORTs above 5000 are usually free to use

`hostname -I`

3. Start the DREAMRNN Predictor with the IP address and PORT arguments

`apptainer run predictor.sif HOST PORT`

Example:
`apptainer run predictor.sif 172.16.47.243 5000`

4. Start the test Evaluator 

```bash 
apptainer run \ 
    -B /path/to/evaluator_data:/evaluator_data  \
    -B /path/to/predictions:/predictions  \
    evaluator.sif HOST PORT /path/to/predictions
```

The `-B` mounts local directories so that the Evaluator container can read in the JSON file from a local folder and write the prediction to the locally created `/predictions` folder.

5. If the Evaluator-Prediction communication was successful a JSON file will be found in the `predictions/` folder.

    