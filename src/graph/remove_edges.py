import threading
from graph.graph import Graph
import networkx as nx
from marginalize import get_marginalize_channel
from utils import get_type_nodes
import pandas as pd


def remove_edges(network: Graph, probabilities, proccess_data):
    for removed_edge in network.edges():
        original_graph = network.copy()
        original_graph.remove_edge(*removed_edge)

        graph_processor = Graph()
        graph_processor.add_edges_to_graph(original_graph.edges())

        if nx.is_connected(graph_processor):
            calcule_probabilities_connect_graph(
                graph_processor, [removed_edge], probabilities, proccess_data)

        else:
            pass


def calcule_probabilities_connect_graph(graph: Graph, removed_edge: list, probabilities, proccess_data):
    prob_expression = graph.conver_edges_to_probability_expression()
    print('Probabilities expression: \n', prob_expression)
    tablet_marginalize = None
    tables_result = {}

    for future, current in prob_expression.items():
        future_expression = future.replace("'", "")
        tablet_marginalize = get_marginalize_channel(
            probabilities[future_expression], current, proccess_data['channels'])
        
        tables_result[future] = tablet_marginalize
    
    for edge in removed_edge:
        complete_table_prob(tables_result, edge, prob_expression)

    print('Tables result: \n', tables_result)


def complete_table_prob(probabilities, node_delete, probability_exp):
    node1, node2 = node_delete
    future, current = get_type_nodes(node1, node2)
    channels_current = probability_exp[future]
    position_change = calcule_position_modify_index(channels_current, current)

    probability_table = probabilities[future]

    probabilities[future] = modify_table_probability(probability_table, position_change)


def modify_table_probability(probability_table, position):
    copy_probability_table = probability_table.copy()   

    probability_table.index = [modify_index(index, position, '0') for index in probability_table.index]
    copy_probability_table.index = [modify_index(index, position, '1') for index in copy_probability_table.index]

    new_probability_table = pd.concat([probability_table, copy_probability_table])

    return new_probability_table



def modify_index(index, position, value):
    index = index[:position] + value + index[position:]
    return index

def calcule_position_modify_index(chanels, node):
    str_chanels = chanels + node
    sorted_channels = ''.join(sorted(str_chanels))
    index_node = sorted_channels.index(node)

    return index_node
    


