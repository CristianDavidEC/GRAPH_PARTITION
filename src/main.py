import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import probability.utils as utils
import partition.partition as partition
from graph.graph import Graph
from graph.remove_edges import remove_edges


def main(process_data):
    #partition.calculate_partition(process_data)

    new_graph = Graph()
    network_graph = new_graph.create_graph(process_data['current'], process_data['future'])
    # print('Edges: \n', network_graph.edges())
    
    nx.draw(network_graph, with_labels=True)
    plt.show()

    probability_distributions = utils.create_probability_distributions(process_data['file'])
    #print('Table Probability: \n' , probability_distributions)

    #custom_remove_edge(network_graph, probability_distributions, process_data)
    remove_edges(network_graph, probability_distributions, process_data)
    
    # full_prob_matriz = get_full_probability_matrix(probability_distributions, process_data['current'])
    # print('\n Full probability matrix: \n', full_prob_matriz)

    # probabilities_values = get_probability_tables(process_data, probability_distributions)
    # print('\n Probabilities values to chanel: \n')
    # print(probabilities_values)

    # table_prob = calculate_joint_probability(probabilities_values)
    # print('\n Probabilities values:')
    # print(table_prob)

    # # Graficar barras
    # graph_probability(table_prob, process_data)

    # pos = nx.spring_layout(network_graph)
    # nx.draw(network_graph, pos, with_labels=True)
    # plt.show()
    

def graph_probability(table_prob, process_data):
    table_prob.plot(x='state', y='probability', kind='bar')
    plt.title(f'State - Probability {process_data['future']} | {process_data['current']} = {process_data['state']}')
    plt.xlabel('State')
    plt.ylabel('Probability')
    plt.ylim(0, 1)
    plt.show()

if __name__ == '__main__':
    data_to_process = {
        'file': 'data/tablex5.json',
        'future': 'ABC',
        'current': 'ABC',
        'state': '100',
        'channels': 'ABCDE',
        #'method': 'partition' # partition | delete_edges | clear_zeros | heuristicas
    }

    # print('Data to process: \n', data_to_process)

    main(data_to_process)


