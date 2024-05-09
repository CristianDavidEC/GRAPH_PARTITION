import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from probability import get_probability_tables, calculate_joint_probability
from utils import create_probability_distributions
from graph.graph import create_graph



def main(process_data):
    network_graph = create_graph(process_data['channels'])
    print(network_graph.edges())
    probability_distributions = create_probability_distributions(process_data['file'])
    # print('Probability distributions: \n', probability_distributions)

    probabilities_values = get_probability_tables(process_data, probability_distributions)
    print('\n Probabilities values to chanel: \n')
    print(probabilities_values)

    table_prob = calculate_joint_probability(probabilities_values)
    print('\n Probabilities values:')
    print(table_prob)

    # Graficar barras
    graph_probability(table_prob, process_data)

    pos = nx.spring_layout(network_graph)
    nx.draw(network_graph, pos, with_labels=True)
    plt.show()
    

def graph_probability(table_prob, process_data):
    table_prob.plot(x='state', y='probability', kind='bar')
    plt.title(f'State - Probability {process_data['future']} | {process_data['current']} = {process_data['state']}')
    plt.xlabel('State')
    plt.ylabel('Probability')
    plt.ylim(0, 1)
    plt.show()

if __name__ == '__main__':
    data_to_process = {
        'file': 'data/prob_table.json',
        'future': 'ABC',
        'current': 'ABC',
        'state': '111',
        'channels': 'ABC'
    }

    # print('Data to process: \n', data_to_process)

    main(data_to_process)


