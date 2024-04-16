import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from patterns import find_patterms
from state_channel import get_matrix_state_channel_f
from probability import get_probability_tables, calculate_probability


def main(process_data):
    # Load data from csv file
    data = pd.read_csv(process_data['file'], dtype=int)
    # print('Data: \n', data)

    # Find patterns
    patterns_found = find_patterms(data)
    # print('\nPatterns found: \n', patterns_found)

    # 1) State Channel F matrix
    print('\n 1) State Channel F matrix')
    matix_states_channel = get_matrix_state_channel_f(patterns_found, data)
    matix_states_channel_df = pd.DataFrame(
        matix_states_channel, index=data.columns)

    matix_final_states = matix_states_channel_df.T
    print(matix_final_states)
    process_data['channels'] = ''.join(data.columns)
    future = process_data['future']
    current = process_data['current']
    state = process_data['state']
    all_channels = process_data['channels']

    print('All channels: ', all_channels)
    print('Future channels: ', future)
    print('Current channels: ', current)
    print('State current channels: ', state)

    probabilities_values = get_probability_tables(process_data, matix_final_states)
    # print('\n Probabilities values: \n')
    # print(probabilities_values)

    table_prob = calculate_probability(probabilities_values)
    print('\n Probabilities values:')
    print(table_prob)

    # Graficar barras
    table_prob.plot(x='state', y='probability', kind='bar')
    plt.title(f'State - Probability {future} | {current} = {state}')
    plt.xlabel('State')
    plt.ylabel('Probability')
    plt.ylim(0, 1)
    plt.show()


if __name__ == '__main__':
    data_to_process = {
        'file': 'data/muestra12.csv',
        'future': '',
        'current': '',
        'state': '10'
    }

    main(data_to_process)
