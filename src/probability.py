from utils import create_sub_table
from marginalize import get_marginalize_channel
import numpy as np
import itertools
import pandas as pd


# The probability of
# P(ABC future | ABC current) = P(A future | ABC current) * P(B future | ABC current) * P(C future | ABC current)
# * -> Tensor product
def calculate_probability(probability_tables):
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
def get_probability_tables(process_data, tabla):
    future_channels = process_data['future']
    current_channels = process_data['current']
    state_current_channels = process_data['state']
    all_channels = process_data['channels']
    probability_tables = {}
    
    if future_channels == '':
        marg_empty_future = get_marginalize_channel(tabla, current_channels, all_channels)
        prom_rows = marg_empty_future.mean(axis=1)
        probability_tables[''] = prom_rows.values

    for f_channel in future_channels:
        sub_table = create_sub_table(tabla, f_channel)
        if current_channels == '':
            probability_tables[f_channel] = get_prob_empty_current(sub_table)
            continue

        table_prob = get_marginalize_channel(
            sub_table, current_channels)
        
        row_probability = table_prob.loc[state_current_channels]
        #print('Row probability: ', row_probability)
        probability_tables[f_channel] = row_probability.values

    return probability_tables


def get_prob_empty_current(table):
    return table.mean(axis=0).values