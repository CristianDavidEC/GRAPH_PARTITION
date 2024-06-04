import numpy as np
import itertools
import pandas as pd
import probability.marginalize as mg
import probability.utils as utils



# The probability of
# P(ABC future | ABC current) = P(A future | ABC current) * P(B future | ABC current) * P(C future | ABC current)
# * -> Tensor product
def calculate_joint_probability(probability_tables):
    prob_array = [probability_tables[key] for key in probability_tables]
    result = prob_array[0]
    combinations = create_index_table(len(prob_array))
    for arr in prob_array[1:]:
        result = np.tensordot(result, arr, axes=0)

    final_table_prob = dict(zip(combinations, result.ravel()))
    df_final_tb = pd.DataFrame.from_dict(final_table_prob, orient='index')
    df_final_tb = df_final_tb.reset_index()
    df_final_tb.columns = ['state', 'probability']

    return df_final_tb

def create_index_table(num_elements):
    combinations = list(itertools.product([0, 1], repeat=num_elements))
    combinations_string = [''.join(map(str, comb)) for comb in combinations]
    
    return combinations_string

## Get the marginalize table for the future channels, with your probabilities in a state channel
def get_probability_tables(process_data, probs_table):
    future_channels = process_data['future']
    current_channels = process_data['current']
    state_current_channels = process_data['state']
    all_channels = process_data['channels']
    probability_tables = {}
    
    if future_channels == '':
        full_matrix = get_original_probability(probs_table, current_channels, future_channels, all_channels)
        maginalize_table = mg.get_marginalize_channel(full_matrix, current_channels, all_channels)

        row_sum = maginalize_table.loc[state_current_channels].sum()
        probability_tables[''] = np.array([row_sum, 1 - row_sum])

    for f_channel in future_channels:
        if current_channels == '':
            probability_tables[f_channel] = get_prob_empty_current(probs_table[f_channel])
            continue

        table_prob = mg.get_marginalize_channel(
            probs_table[f_channel], current_channels, all_channels)
        
        row_probability = table_prob.loc[state_current_channels]
        probability_tables[f_channel] = row_probability.values

    return probability_tables


def get_prob_empty_current(table):
    return table.mean(axis=0).values


def get_original_probability(probs_table, current_channels, future_channels, all_channels):
    marg_table = {}

    for key, table in probs_table.items():
        if key in future_channels:
            new_table = mg.get_marginalize_channel(table, current_channels, all_channels)
            marg_table[key] = new_table

    index_tables = marg_table[current_channels[0]].index
    n_cols = 2 ** len(future_channels)
    full_matriz = pd.DataFrame(columns=[f'{key}' for key in range(n_cols)])

    for index in index_tables:
        prob_state = {}
        for key, table in marg_table.items():
            value = table.loc[index].values
            prob_state[key] = value
        
        joint_prob = calculate_joint_probability(prob_state)
        columns = joint_prob['state'].values
        full_matriz.columns = columns
        full_matriz.loc[index] = joint_prob['probability'].values


    return full_matriz
        
    
    

    