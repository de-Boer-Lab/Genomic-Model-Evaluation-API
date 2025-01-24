# api_preprocessing_utils.py

## model specific checks that cause a "prediction_request_failed" error
def check_seqs_specifications(sequences, json_return_error_model):
    max_length = 2000
    for sequence in sequences:
        value = sequences[sequence]
        key = sequence

        if len(value) > 2000:
            json_return_error_model['prediction_request_failed'].append("length of a sequence in " + key + " is greater than 2000")
        if "N" in value:
            json_return_error_model['prediction_request_failed'].append("sequence in " + key + " has an invalid character present")
    return(json_return_error_model)

# One-hot encode sequences
def one_hot_encode(seq):
    """
    Convert a sequence to a one-hot encoded representation.

    Args:
        seq (str): Sequence consisting of 'A', 'T', 'G', 'C', and 'N'.

    Returns:
        list: A one-hot encoded list for the sequence.
    """
    mapping = {'A': [1, 0, 0, 0],
               'G': [0, 1, 0, 0],
               'C': [0, 0, 1, 0],
               'T': [0, 0, 0, 1],
               'N': [0, 0, 0, 0]}
    return [mapping.get(base, [0, 0, 0, 0]) for base in seq]

# Pad or truncate sequences to match a fixed sequence size
def process_sequence(seq, seq_size=230):
    """
    One-hot encode a sequence and centre-pad or truncate it to a fixed size.

    Args:
        seq (str): Sequence consisting of 'A', 'T', 'G', 'C', and 'N'.
        seq_size (int): Fixed length to pad or truncate the sequence.

    Returns:
        list: A one-hot encoded list with padding or truncation applied.
    """
    encoded_seq = one_hot_encode(seq)
    seq_len = len(encoded_seq)
    
    if seq_len > seq_size:
        # Truncate if the sequence is too long
        return encoded_seq[:seq_size]  
    
    # if seq_len > seq_size:
    #     # Truncate equally from both ends -- uncomment this, if needed.
    #     start_idx = (seq_len - seq_size) // 2
    #     return encoded_seq[start_idx:start_idx + seq_size]
    
    else:
        # Centre-pad with zeros if the sequence is too short
        # left_padding and right_padding are calculated to distribute padding equally on both sides.
        # If there’s an odd number of extra padding, the right side gets the additional padding.
        total_padding = seq_size - seq_len
        left_padding = [[0, 0, 0, 0]] * (total_padding // 2)
        right_padding = [[0, 0, 0, 0]] * (total_padding - len(left_padding))
        return left_padding + encoded_seq + right_padding
    # Swtich left right padding