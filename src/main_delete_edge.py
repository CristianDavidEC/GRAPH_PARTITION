import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import probability.utils as utils
from graph.graph import Graph
from graph.remove_edges import remove_edges


def main(process_data):
    new_graph = Graph()
    network_graph = new_graph.create_graph(process_data['current'], process_data['future'])
        
    nx.draw(network_graph, with_labels=True)
    plt.show()

    probability_distributions = utils.create_probability_distributions(process_data['file'])

    #custom_remove_edge(network_graph, probability_distributions, process_data)
    remove_edges(network_graph, probability_distributions, process_data)
    


if __name__ == '__main__':
    data_to_process = {
        #'file': 'src/data/tablex5.json',
        'file': 'data/tablex5.json',
        'future': 'BC',
        'current': 'ABC',
        'state': '100',
        'channels': 'ABCDE',
        #'method': 'partition' # partition | delete_edges | clear_zeros | heuristicas
    }

    # print('Data to process: \n', data_to_process)

    main(data_to_process)


