import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from probability import get_probability_tables, calculate_joint_probability, get_full_probability_matrix
from utils import create_probability_distributions
from graph.graph import Graph
from graph.remove_edges import remove_edges


def main(process_data):
    new_graph = Graph()
    network_graph = new_graph.create_graph(process_data['channels'])    
    print('Edges: \n', network_graph.edges())

    probability_distributions = create_probability_distributions(process_data['file'])
    print('Table Probability: \n' , probability_distributions)


    #remove_edges(network_graph, process_data)
        
    
    full_prob_matriz = get_full_probability_matrix(probability_distributions, process_data['current'])
    print('\n Full probability matrix: \n', full_prob_matriz)

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
        'current': 'BC',
        'state': '11',
        'channels': 'ABC'
    }

    # print('Data to process: \n', data_to_process)

    main(data_to_process)


