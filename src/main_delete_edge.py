import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import probability.utils as utils
from graph.graph import Graph
from graph.remove_edges import remove_edges


def main_delete_edge(process_data):
    new_graph = Graph()
    network_graph = new_graph.create_graph(process_data['current'], process_data['future'])
    original_graph = network_graph.copy()
        
    probability_distributions = utils.create_probability_distributions(process_data['file'])
    neteork_found = remove_edges(network_graph, probability_distributions, process_data)

    print('--------- Results ---------')
    print(f'Loss value: {neteork_found.loss_value}')
    print(f'Removed edges: {neteork_found.removed_edges}')
    print(f'Edges Result: {neteork_found.edges(data=True)}')

    utils.graph_result(original_graph, neteork_found)


if __name__ == '__main__':
    data_to_process = {
        'file': 'data/tablex5.json',
        'future': 'ABCDE',
        'current': 'ABCDE',
        'state': '10001',
        'channels': 'ABCDE',
        #'method': 'partition' # partition | delete_edges | clear_zeros | heuristicas
    }

    main_delete_edge(data_to_process)


