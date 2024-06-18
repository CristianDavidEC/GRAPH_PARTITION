import threading
from graph.graph import Graph
import networkx as nx
import pandas as pd
from probability.marginalize import get_marginalize_channel
from probability.utils import get_type_nodes
import probability.probability as prob
import emd.emd_calculation as emd
import matplotlib.pyplot as plt
import graph.find_partition as partition

# Evalua cada uno de los edges del grafo, eliminandolo y calculando su nueva probabilidad y valor de perdida.
# si encuentra un 0, elimina el edge, si eliminando los edge el grafo deja de ser conexo, retorna la particion con perdida 0
# de lo contrario calcula la perdida del grafo eliminando combos de aristas.
def remove_edges(network: Graph, probabilities, proccess_data):
    original_prob = prob.get_original_probability(
        probabilities, proccess_data['current'], proccess_data['future'], proccess_data['channels'])

    original_graph = network.copy()

    for removed_edge in original_graph.edges():
        graph_processor = create_new_graph(original_graph, removed_edge)
        calcule_probability_dist(
            graph_processor, probabilities, proccess_data)

        emd_value = emd.calcule_emd(
            graph_processor, proccess_data['state'], original_prob)
        graph_processor.loss_value = emd_value

        original_graph[removed_edge[0]][removed_edge[1]]['weight'] = emd_value
        network[removed_edge[0]][removed_edge[1]]['weight'] = emd_value

        if graph_processor.loss_value == 0:
            network.remove_edge(*removed_edge)
            network.removed_edges.append(removed_edge)

        if not nx.is_connected(network):
            network.loss_value = emd_value

            return network

    delete_zeros_graph(original_graph, probabilities, proccess_data)
    edge_found = partition.find_best_partition(
        original_graph, proccess_data, original_prob)

    return edge_found


# Una vez calculado el valor de todas las aristas y no encontrar una particion
# con perdida 0, se elimina los edge de perdida 0 y crea un nuevo grafo con los restantes y sus respectivas perdidas
def delete_zeros_graph(network: Graph, probabilities, proccess_data):
    original_prob = prob.get_original_probability(
        probabilities, proccess_data['current'], proccess_data['future'], proccess_data['channels'])

    network.table_probability = probabilities
    graph_processor = network.copy()

    for node1, node2, details_edge in graph_processor.edges(data=True):
        if details_edge['weight'] == 0:
            network.remove_edge(node1, node2)
            network.removed_edges.append((node1, node2, details_edge['weight']))
            calcule_probability_dist(
                network, probabilities, proccess_data)

    modify_tables = {key.replace(
        "'", ""): value for key, value in network.table_probability.items()}
    network.table_probability = modify_tables


# Crea un nuevo grafo removiendo el borde
def create_new_graph(network: Graph, removed_edge):
    node1, node2, *reset = removed_edge
    original_graph = network.copy()
    original_graph.remove_edge(node1, node2)

    graph_processor = Graph()
    graph_processor.add_edges_to_graph(original_graph.edges(data=True))
    graph_processor.removed_edges.append(removed_edge)

    return graph_processor


# Calcula la nueva tabla de probabilidad del grafo sin el edge
# @ param probabilities: diccionario con las tablas de probabilidad original
# @ param graph: grafo con los edges removidos
# @ param proccess_data: diccionario con los datos del proceso
def calcule_probability_dist(graph: Graph, probabilities, proccess_data):
    prob_expression = graph.conver_edges_to_probability_expression()
    tablet_marginalize = None
    tables_result = {}
    size_current = len(proccess_data['current'])
    result_empty_future = {}

    for future, current in prob_expression.items():
        future_expression = future.replace("'", "")
        tablet_marginalize = get_marginalize_channel(
            probabilities[future_expression], current, proccess_data['channels'])

        tables_result[future] = tablet_marginalize

    for edge in graph.removed_edges:
        node1, node2, *reset = edge
        future, current = get_type_nodes(node1, node2)

        # Calcula la probabilidad para el caso futuro vacio | current
        if future not in tables_result:
            table, prob_exp = get_table_future_empty(
                (future, current), probabilities, proccess_data)
            result_empty_future[future] = table
            complete_table_prob(result_empty_future, edge,
                                prob_exp, size_current)
            probabilities[future] = table
        else:
            complete_table_prob(tables_result, edge,
                                prob_expression, size_current)

        # Calcula la probabilidad para el caso futuro | current vacio
        if size_current == 1:
            node1, node2 = edge
            future, current = get_type_nodes(node1, node2)
            key_future = future.replace("'", "")

            table_future = probabilities[key_future].mean(axis=0).values
            tables_result[future] = table_future

    merge_results = {**result_empty_future, **tables_result}
    graph.table_probability = merge_results


# Calcula la tabla de probabilidad cuando la expresion de probabilidad no encuentra
# una expresion para el nodo eliminado, este caso equivale al futuro vacio | current
def get_table_future_empty(node_delete, probabilities, proccess_data):
    future, current = node_delete
    currents = proccess_data['current'].replace(current, "")
    exp_prob = {}

    chat_future = future.replace("'", "")
    marginalize_table = get_marginalize_channel(
        probabilities[chat_future], currents, proccess_data['channels'])

    exp_prob[future] = currents

    return marginalize_table, exp_prob


# Rellena el valor marginalizado de la tabla, "Copiando" el valor de probabilidad
# marguinalizado a la tabla como si tuviera todos sus valores originales.
# @ param probabilities: diccionario con las tablas de probabilidad
# @ param node_delete: tupla con los nodos a eliminar
# @ param probability_exp: diccionario con las expresiones de probabilidad, del grafo sin los nodos eliminados
def complete_table_prob(probabilities, node_delete, probability_exp, size_current=0):
    node1, node2, *reset = node_delete
    future, current = get_type_nodes(node1, node2)

    if size_current == 1:
        return
    channels_current = probability_exp[future]
    position_change = calcule_position_modify_index(channels_current, current)

    probability_table = probabilities[future]

    probabilities[future] = modify_table_probability(
        probability_table, position_change)


# Copia la tabla de probabilidad con el resultado de la marginalizacion
# @ param probability_table: tabla de probabilidad
# @ param position: posicion a modificar
# El posicion es el indice del caracter a modificar
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


# Dados todos los current channels, y el nodo eliminado, determina en que posicion de la cadena
# debe el el caracter a agregar en la indice de la tabla a modificar
def calcule_position_modify_index(chanels, node):
    str_chanels = chanels + node
    sorted_channels = ''.join(sorted(str_chanels))
    index_node = sorted_channels.index(node)

    return index_node
