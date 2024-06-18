import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import probability.utils as utils
from graph.graph import Graph
from graph.remove_edges import remove_edges
import time as t


def main_delete_edge(process_data):
    new_graph = Graph()
    network_graph = new_graph.create_graph(process_data['current'], process_data['future'])
    original_graph = network_graph.copy()
        
    init = t.time()
    probability_distributions = utils.create_probability_distributions(process_data['file'])
    neteork_found = remove_edges(network_graph, probability_distributions, process_data)

    finish = t.time()

    print('--------- Results ---------')
    print(f'Loss value: {neteork_found.loss_value}')
    print(f'Removed edges: {neteork_found.removed_edges}')
    print(f'Edges Result: {neteork_found.edges(data=True)}')
    print(f'Components: {list(nx.connected_components(neteork_found))}')
    print(f'Time: {finish - init} \n\n')

    print(f'Probability distributions: {neteork_found.table_probability}')



    utils.graph_result(original_graph, neteork_found)



