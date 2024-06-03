import threading
from graph.graph import Graph
import networkx as nx
import pandas as pd
from probability.marginalize import get_marginalize_channel
from probability.utils import get_type_nodes
import probability.probability as prob
import graph.emd_calculation as emd


def remove_edges(network: Graph, probabilities, proccess_data):
    original_prob = prob.get_original_probability(
        probabilities, proccess_data['channels'])

    print(original_prob)

    for removed_edge in network.edges():
        original_graph = network.copy()
        original_graph.remove_edge(*removed_edge)

        graph_processor = Graph()
        graph_processor.add_edges_to_graph(original_graph.edges())
        graph_processor.removed_edges.append(removed_edge)

        if nx.is_connected(graph_processor):
            calcule_probability_dist(
                graph_processor, probabilities, proccess_data)

            emd_value = emd.calcule_emd(
                graph_processor, proccess_data['state'], original_prob)
            graph_processor.loss_value = emd_value

            print(f'''Information Graph
    EDGES:
    {graph_processor.edges}
    REMOVED EDGE:
    {graph_processor.removed_edges}
    VALE LOSS  
    {graph_processor.loss_value}
                  ''')
        else:
            pass


def custom_remove_edge(network: Graph, probabilities, proccess_data):
    original_prob = prob.get_original_probability(
        probabilities, proccess_data['channels'])

    #print(original_prob)
    removes_edges = [("A", "B'"), ("C", "A'"), ("B", "B'")]
    #removes_edges = [("A", "B'"), ("B", "B'")]

    for removed_edge in removes_edges:
        network.remove_edge(*removed_edge)

    graph_processor = Graph()
    graph_processor.add_edges_to_graph(network.edges())
    graph_processor.removed_edges = removes_edges

    if nx.is_connected(graph_processor):
        print(f'Grafo Conexo\n {vars(graph_processor)}')
        print(f'Edges\n {graph_processor.edges}')
        calcule_probability_dist(
            graph_processor, probabilities, proccess_data)

        emd_value = emd.calcule_emd(
            graph_processor, proccess_data['state'], original_prob)
        graph_processor.loss_value = emd_value

        print(f'''Information Graph
    EDGES:
    {graph_processor.edges}
    REMOVED EDGE:
    {graph_processor.removed_edges}
    VALE LOSS  
    {graph_processor.loss_value}
                  ''')
    else:
        print('Grafo No Conexo')
        pass


def calcule_probability_dist(graph: Graph, probabilities, proccess_data):
    prob_expression = graph.conver_edges_to_probability_expression()
    tablet_marginalize = None
    tables_result = {}

    print(f'Expresion de probabilidad: {prob_expression}')

    for future, current in prob_expression.items():
        future_expression = future.replace("'", "")
        tablet_marginalize = get_marginalize_channel(
            probabilities[future_expression], current, proccess_data['channels'])

        tables_result[future] = tablet_marginalize

    for edge in graph.removed_edges:
        complete_table_prob(tables_result, edge, prob_expression)

    graph.table_probability = tables_result


def complete_table_prob(probabilities, node_delete, probability_exp):
    node1, node2 = node_delete
    future, current = get_type_nodes(node1, node2)
    channels_current = probability_exp[future]
    position_change = calcule_position_modify_index(channels_current, current)

    probability_table = probabilities[future]

    probabilities[future] = modify_table_probability(
        probability_table, position_change)


def modify_table_probability(probability_table, position):
    copy_probability_table = probability_table.copy()

    probability_table.index = [modify_index(
        index, position, '0') for index in probability_table.index]
    copy_probability_table.index = [modify_index(
        index, position, '1') for index in copy_probability_table.index]

    new_probability_table = pd.concat(
        [probability_table, copy_probability_table])

    return new_probability_table


def modify_index(index, position, value):
    index = index[:position] + value + index[position:]
    return index


def calcule_position_modify_index(chanels, node):
    str_chanels = chanels + node
    sorted_channels = ''.join(sorted(str_chanels))
    index_node = sorted_channels.index(node)

    return index_node
