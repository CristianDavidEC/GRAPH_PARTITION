import threading
from graph.graph import Graph
import networkx as nx
import pandas as pd
from probability.marginalize import get_marginalize_channel
from probability.utils import get_type_nodes
import probability.probability as prob
import graph.emd_calculation as emd
import matplotlib.pyplot as plt


def remove_edges(network: Graph, probabilities, proccess_data):
    original_prob = prob.get_original_probability(
        probabilities, proccess_data['current'], proccess_data['future'], proccess_data['channels'])

    original_graph = network.copy()

    for removed_edge in original_graph.edges():
        graph_processor = create_new_graph(original_graph, removed_edge)
        calcule_probability_dist(
            graph_processor, probabilities, proccess_data)
        
        # print('Nodes:', graph_processor.nodes())
        # print('Edges:', graph_processor.edges())    

        emd_value = emd.calcule_emd(
            graph_processor, proccess_data['state'], original_prob)
        graph_processor.loss_value = emd_value

        # print(f'''Information Graph
        #         EDGES:
        #         {graph_processor.edges}
        #         REMOVED EDGE:
        #         {graph_processor.removed_edges}
        #         VALE LOSS: {graph_processor.loss_value}
        #         ''')
        original_graph[removed_edge[0]][removed_edge[1]]['weight'] = emd_value

        if graph_processor.loss_value == 0:
            network.remove_edge(*removed_edge)
            network.removed_edges.append(removed_edge)

        if not nx.is_connected(network):
            network.loss_value = emd_value
            print(f'Grafo Conexo\n {vars(original_graph)}')
            print(f'Grafo no Conexo\n {vars(network)}')

            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

            nx.draw(original_graph, with_labels=True, ax=ax1)
            nx.draw(network, with_labels=True, ax=ax2)

            plt.show()

            return
    
    print(f'Grafo con eliminaciones: \n {vars(network)}')
    print('Grafo completo')
    print(f'Edges\n {original_graph.edges(data=True)}')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    nx.draw(original_graph, with_labels=True, ax=ax1)
    nx.draw(network, with_labels=True, ax=ax2)
    plt.show()

    pos = nx.spring_layout(original_graph)
    nx.draw(original_graph, pos, with_labels=True, node_color='lightblue', edge_color='gray')
    labels = nx.get_edge_attributes(original_graph, 'weight')
    nx.draw_networkx_edge_labels(original_graph, pos, edge_labels=labels)
    plt.show()
    


# def custom_remove_edge(network: Graph, probabilities, proccess_data):
#     original_prob = prob.get_original_probability(
#         probabilities, proccess_data['current'], proccess_data['future'], proccess_data['channels'])

#     #print(original_prob)
#     removes_edges = [("A", "A'"), ("C", "A'")]

#     for removed_edge in removes_edges:
#         network.remove_edge(*removed_edge)

#     graph_processor = Graph()
#     graph_processor.add_edges_to_graph(network.edges())
#     graph_processor.removed_edges = removes_edges

#     if nx.is_connected(graph_processor):
#         print(f'Grafo Conexo\n {vars(graph_processor)}')
#         print(f'Edges\n {graph_processor.edges}')
#         calcule_probability_dist(
#             graph_processor, probabilities, proccess_data)

#         emd_value = emd.calcule_emd(
#             graph_processor, proccess_data['state'], original_prob)
#         graph_processor.loss_value = emd_value

#         print(f'''Information Graph
#     EDGES:
#     {graph_processor.edges}
#     REMOVED EDGE:
#     {graph_processor.removed_edges}
#     VALE LOSS  
#     {graph_processor.loss_value}
#                   ''')
#     else:
#         print('Grafo No Conexo')
#         pass


### Crea un nuevo grafo con el edge removido
def create_new_graph(network: Graph, removed_edge):
    original_graph = network.copy()
    original_graph.remove_edge(*removed_edge)

    graph_processor = Graph()
    graph_processor.add_edges_to_graph(original_graph.edges())
    graph_processor.removed_edges.append(removed_edge)

    return graph_processor


### Calcula la nueva tabla de probabilidad del grafo sin el edge
### @ param probabilities: diccionario con las tablas de probabilidad original
def calcule_probability_dist(graph: Graph, probabilities, proccess_data):
    prob_expression = graph.conver_edges_to_probability_expression()
    tablet_marginalize = None
    tables_result = {}
    
    for future, current in prob_expression.items():
        future_expression = future.replace("'", "")
        tablet_marginalize = get_marginalize_channel(
            probabilities[future_expression], current, proccess_data['channels'])

        tables_result[future] = tablet_marginalize

    
    # print(len(proccess_data['current']))
    # if len(proccess_data['current']) == 1:
    #     graph.table_probability = tables_result

    #     return

    for edge in graph.removed_edges:
        complete_table_prob(tables_result, edge, prob_expression)

    graph.table_probability = tables_result



### Rellena el valor marginalizado de la tabla, "Copiando" el valor de probabilidad 
### marguinalizado a la tabla como si tuviera todos sus valores originales.
### @ param probabilities: diccionario con las tablas de probabilidad
### @ param node_delete: tupla con los nodos a eliminar
### @ param probability_exp: diccionario con las expresiones de probabilidad, del grafo sin los nodos eliminados
def complete_table_prob(probabilities, node_delete, probability_exp, size_current=0):
    print(probabilities)
    print(probability_exp)
    print(node_delete)
    node1, node2 = node_delete
    future, current = get_type_nodes(node1, node2)

    if size_current == 0:
        return

    channels_current = probability_exp[future]
    position_change = calcule_position_modify_index(channels_current, current)

    probability_table = probabilities[future]

    probabilities[future] = modify_table_probability(
        probability_table, position_change)


### Copia la tabla de probabilidad con el resultado de la marginalizacion
### @ param probability_table: tabla de probabilidad
### @ param position: posicion a modificar
### El posicion es el indice del caracter a modificar
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


### Dados todos los current channels, y el nodo eliminado, determina en que posicion dela cadena
### debe el el caracter a agregar en la indice de la tabla a modificar
def calcule_position_modify_index(chanels, node):
    str_chanels = chanels + node
    sorted_channels = ''.join(sorted(str_chanels))
    index_node = sorted_channels.index(node)

    return index_node