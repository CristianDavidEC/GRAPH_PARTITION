import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import probability.utils as utils
import partition.partition as partition
from graph.graph import Graph
from graph.remove_edges import remove_edges


def main_partition(process_data):
    original_graph = Graph().create_graph(process_data['current'], process_data['future'])

    partition_found = partition.calculate_partition(process_data)
    graph_found = get_graph(partition_found)
    graph_found.loss_value = partition_found['value']

    print('--------- Results ---------')
    print(vars(graph_found))


    utils.graph_result(original_graph, graph_found)


def get_graph(partition_graph):
    partition = partition_graph['partition']
    partition1, partition2 = partition

    graph1 = create_graph(partition1)
    graph2 = create_graph(partition2)
    merged_graph = nx.compose(graph1, graph2)

    graph_result = Graph()
    graph_result.add_edges_from(merged_graph.edges(data=True))
    graph_result.add_nodes_from(merged_graph.nodes(data=True))

    return graph_result

def create_graph(partition):
    future, current = partition
    graph = Graph().create_graph(current, future)

    return graph


if __name__ == '__main__':
    data_to_process = {
        #'file': 'src/data/tablex5.json',
        'file': 'data/tablex5.json',
        'future': 'ABC',
        'current': 'AC',
        'state': '10',
        'channels': 'ABCDE',
        #'method': 'partition' # partition | delete_edges | clear_zeros | heuristicas
    }

    main_partition(data_to_process)


