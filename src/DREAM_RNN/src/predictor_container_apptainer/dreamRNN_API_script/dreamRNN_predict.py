# dreamRNN_predict.py
#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import torch
import numpy as np
import os
import sys
import tqdm

# Get the current working directory
CWD = os.getcwd()

# Determine if running inside a container or not
if os.path.exists('/predictor_container_apptainer'):
    # Running inside the container
    BASE_DIR = os.path.join(CWD, 'dreamRNN_API_script')
    UTILS_DIR = os.path.join(CWD, 'predictor_container_apptainer')
else:
    # Running outside the container
    BASE_DIR = os.path.join(CWD, '..', 'dreamRNN_API_script')
    UTILS_DIR = os.path.join(CWD, 'scripts_and_utils')

# Add the directory containing `api_preprocessing_utils.py` to the Python path
sys.path.append(UTILS_DIR)

# Import the process_sequence function
from api_preprocessing_utils import process_sequence

# Define the model directory
MODEL_DIR = os.path.join(BASE_DIR, 'dream_rnn_k562_model_weight')

# Import prixfixe framework
from prixfixe.autosome import AutosomeFinalLayersBlock
from prixfixe.bhi import BHIFirstLayersBlock
from prixfixe.bhi import BHICoreBlock
from prixfixe.prixfixe import PrixFixeNet

# initialize path and variables
CUDA_DEVICE_ID = 0
SEQ_SIZE = 230
generator = torch.Generator()
generator.manual_seed(42)
device = torch.device(f"cuda:{CUDA_DEVICE_ID}" if torch.cuda.is_available() else "cpu")

# Model Definition For Dream-RNN
def build_dream_rnn():
    first = BHIFirstLayersBlock(
        in_channels = 5,
        out_channels = 320,
        seqsize = SEQ_SIZE,
        kernel_sizes = [9, 15],
        pool_size = 1,
        dropout = 0.2
    )

    core = BHICoreBlock(
        in_channels = first.out_channels,
        out_channels = 320,
        seqsize = first.infer_outseqsize(),
        lstm_hidden_channels = 320,
        kernel_sizes = [9, 15],
        pool_size = 1,
        dropout1 = 0.2,
        dropout2 = 0.5
    )

    final = AutosomeFinalLayersBlock(
        in_channels=core.out_channels,
        seqsize=core.infer_outseqsize()
    )

    model_rnn = PrixFixeNet(
        first=first,
        core=core,
        final=final,
        generator=generator
    )
    return model_rnn

# Load Pre-Trained Model Weights for DREAM-RNN
def load_dream_rnn():
    model = build_dream_rnn()
    model.load_state_dict(torch.load(f"{MODEL_DIR}/model_best.pth",
                                     map_location=device))
    model.to(device)
    model.eval()
    return model

# Hardcoded Upstream and Downstream Adapter Sequences for K562 and HepG2:
TARGET_LENGTH = 200
upstream_adapter_seq = "AGGACCGGATCAACT"
downstream_adapter_seq = "CATTGCGTGAACCGA"

# Prediction Function
def predict_dream_rnn(sequences, include_rev):
    
    """
    Predict expression values using the DREAM-RNN model.

    Args:
        sequences (dict): Dictionary of sequence IDs and their corresponding sequences.
        include_rev (bool): Whether to include the reverse complement flag in the input.

    Returns:
        predictions (dict): Dictionary of sequence IDs and their predicted expression values.
    """
    
    model_rnn = load_dream_rnn()
    
    predictions = {}
    # Wrap the iteration with tqdm for a progress bar
    for seq_id, seq in tqdm.tqdm(sequences.items(),
                                 desc="Predictions in progress", unit="sequence"):
        # Process sequence for padding or truncation
        encoded_seq = process_sequence(seq, TARGET_LENGTH, SEQ_SIZE,
                     upstream_adapter_seq, downstream_adapter_seq)
        
        # Include reverse complement information on sequence ID
        if include_rev:
            rev_flag = 1 if "Reversed" in seq_id else 0
            rev_value = [rev_flag] * len(encoded_seq)
        else:
            rev_value = [0] * len(encoded_seq) # Default to no reverse complement info
            
        # Combine one-hot encoding with reverse flag
        encoded_seq_with_rev = [list(encoded_base) + [rev] for encoded_base,
                                rev in zip(encoded_seq, rev_value)]
    
        # Predict expression values using the model
        # Convert to tensor for prediction
        seq_tensor = torch.tensor(
            np.array(encoded_seq_with_rev).reshape(1, SEQ_SIZE, 5).transpose(0, 2, 1),
            device=device,
            dtype=torch.float32
        )
        
        pred = model_rnn(seq_tensor)
        predictions[seq_id] = pred.detach().cpu().flatten().tolist()
    
    return predictions

# Training function has been removed, given the scope of this API
