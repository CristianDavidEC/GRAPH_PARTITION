import numpy as np
import itertools
import pandas as pd
import probability.marginalize as mg
import probability.utils as utils
from concurrent.futures import ThreadPoolExecutor


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

# Get the marginalize table for the future channels, with your probabilities in a state channel


def get_probability_tables(process_data, probs_table):
    future_channels = process_data['future']
    current_channels = process_data['current']
    state_current_channels = process_data['state']
    all_channels = process_data['channels']
    probability_tables = {}

    if future_channels == '':
        full_matrix = get_original_probability(
            probs_table, current_channels, future_channels, all_channels)
        maginalize_table = mg.get_marginalize_channel(
            full_matrix, current_channels, all_channels)

        row_sum = maginalize_table.loc[state_current_channels].sum()
        probability_tables[''] = np.array([row_sum, 1 - row_sum])

    for f_channel in future_channels:
        if current_channels == '':
            probability_tables[f_channel] = get_prob_empty_current(
                probs_table[f_channel])
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
            new_table = mg.get_marginalize_channel(
                table, current_channels, all_channels)
            marg_table[key] = new_table

    key_index = next(iter(marg_table))
    index_tables = marg_table[key_index].index
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


def get_probability_tables_partition(process_data, probs_table, table_comb, original_prob=None):
    future_channels = process_data['future']
    current_channels = process_data['current']
    state_current_channels = process_data['state']
    all_channels = process_data['channels']
    probability_tables = {}
    original_channels = process_data['original_channels']

    key_comb = future_channels+'|'+current_channels
    print('---------------------')
    print('Key Combo:', key_comb)

    if future_channels == '':
        result = get_future_empty(
            original_prob, current_channels, original_channels, state_current_channels)
        probability_tables[''] = result
        if not table_comb[key_comb]:
            table_comb[key_comb] = probability_tables

        return table_comb[key_comb]

    for f_channel in future_channels:
        key = f_channel + '|' + current_channels
        retult_table = {}
        if table_comb[key]:
            probability_tables.update(table_comb[key])
            continue

        if current_channels == '':
            result = get_prob_empty_current(probs_table[f_channel])
            probability_tables[f_channel] = result
            if not table_comb[key]:
                table_comb[key] = probability_tables
            continue

        table_prob = mg.get_marginalize_channel(
            probs_table[f_channel], current_channels, all_channels)

        row_probability = table_prob.loc[state_current_channels]
        retult_table[f_channel] = row_probability.values
        probability_tables.update(retult_table)
        if not table_comb[key]:
            table_comb[key] = retult_table

    if not table_comb[key_comb]:
        table_comb[key_comb] = probability_tables

    return table_comb[key_comb]


def original_probability_partition(probs_table, current_channels, future_channels, all_channels):
    marg_table = {}
    for key, table in probs_table.items():
        if key in future_channels:
            new_table = mg.get_marginalize_channel(
                table, current_channels, all_channels)
            marg_table[key] = new_table

    key_index = next(iter(marg_table))
    index_tables = marg_table[key_index].index
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


def tensor_product_partition(partition_left, partition_right, parts_exp):
    part_left, part_right = parts_exp
    positions_channels = get_posicion_elements(part_left[0], part_right[0])
    retult = []

    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(
                compute_tensor_product, left, right, parts_exp, positions_channels)
            for _, left in partition_left.iterrows()
            for _, right in partition_right.iterrows()
        ]

        for future in futures:
            response = future.result()
            retult.append(response)

    df_results = pd.DataFrame(retult, columns=['state', 'probability'])

    return df_results


def compute_tensor_product(part_left, part_right, parts_exp, positions):
    tensor_product = part_left['probability'] * part_right['probability']
    index_product = get_index_product(
        part_left['state'], part_right['state'], positions, parts_exp[0])

    result = [index_product, tensor_product]

    return result


def get_index_product(state_left, state_right, positions, parts_exp):
    part_let_future = parts_exp[0]
    if part_let_future == "": return state_right

    result_string = list(state_left)

    for index, char in zip(positions, state_right):
        result_string.insert(index, char)

    return ''.join(result_string)


def get_posicion_elements(channels_left, channels_right):
    unit_channels = ''.join(set(channels_left + channels_right))
    order_channels = ''.join(sorted(unit_channels))

    positions_channels = tuple(order_channels.index(char)
                               for char in channels_right)

    return positions_channels


def get_future_empty(original_prob, current_channels, original_channels, state_current_channels):
    maginalize_table = mg.get_marginalize_channel(
        original_prob, current_channels, original_channels)
    row_sum = maginalize_table.loc[state_current_channels].sum()
    result = np.array([row_sum])

    return result
