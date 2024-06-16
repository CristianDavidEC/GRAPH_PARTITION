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
    original_graph = network_graph.copy()
        
    probability_distributions = utils.create_probability_distributions(process_data['file'])
    neteork_found = remove_edges(network_graph, probability_distributions, process_data)


    print(neteork_found.edges(data=True))
    print(neteork_found.loss_value)
    print(neteork_found.removed_edges)
    print(vars(neteork_found))

    graph_result(original_graph, neteork_found)


def graph_result(original_graph, neteork_found):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    nx.draw(original_graph, with_labels=True, ax=ax1)
    ax1.set_title('Original Network')

    pos = nx.spring_layout(neteork_found)
    edge_labels = nx.get_edge_attributes(G=neteork_found, name='weight')
    edge_labels = {k: f"{v:.1f}" for k, v in edge_labels.items()}
    nx.draw(neteork_found, pos, with_labels=True, ax=ax2)
    nx.draw_networkx_edge_labels(neteork_found, pos, edge_labels=edge_labels, font_size=8, ax=ax2)
    ax2.set_title('Network Best Partition')
    text = 'EMD: ' + str(neteork_found.loss_value)
    ax2.text(0, 0, text, verticalalignment='center', transform=ax2.transAxes)

    plt.show()


if __name__ == '__main__':
    data_to_process = {
        #'file': 'src/data/tablex5.json',
        'file': 'data/tablex5.json',
        'future': 'ABC',
        'current': 'ABC',
        'state': '100',
        'channels': 'ABCDE',
        #'method': 'partition' # partition | delete_edges | clear_zeros | heuristicas
    }

    # print('Data to process: \n', data_to_process)

    main(data_to_process)


