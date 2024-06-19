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
    netework_found = remove_edges(network_graph, probability_distributions, process_data)

    finish = t.time()

    print('--------- Results ---------')
    print(f'Loss value: {netework_found.loss_value}')
    print(f'Removed edges: {netework_found.removed_edges}')
    print(f'Edges Result: {netework_found.edges(data=True)}')
    print(f'Components: {list(nx.connected_components(netework_found))}')
    print(f'Probability distributions: \n {netework_found.table_probability}')
    print(f'Time: {round(finish - init, 5)} \n\n')

    

    utils.graph_result(original_graph, netework_found)



