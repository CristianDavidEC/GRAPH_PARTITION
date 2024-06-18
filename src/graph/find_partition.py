from graph.graph import Graph
import emd.emd_calculation as emd
import graph.remove_edges as remove_edges
import networkx as nx
import probability.utils as utils


# Busca una particion de mejor perdida, eliminando grupos de aristas hasta encontrar
# la que su valor de perdida sea menor.
# @ param network: grafo con las aristas 0 eliminadas
# @ return: grafo con la mejor particion
# Mientras no hay solucion recore lista de grafos a evaluar
# Estos se ordenan por perdida y aristas eliminadas
# Una vez evaluados, revisa su hay solucion y retorna la mejor encontrada
def find_best_partition(network: Graph, proccess_data, original_prob):
    network.loss_value = 0
    val_cup = calcule_cut_value(network, len(proccess_data['current']))
    proccess_data['channels'] = proccess_data['current']
    proccess_data['val_cup'] = val_cup
    best_solutions = []
    graphs_evaluated = [network]
    graph_solition = None

    #is_solution = False
    while len (graphs_evaluated) > 0:
        graphs_evaluated = [
            obj for obj in graphs_evaluated if not obj.evaluated]

        graphs_sort = sorted(graphs_evaluated, key=lambda graph: (
            graph.loss_value, len(graph.removed_edges)))

        for graph in graphs_sort:
            edges_graph = graph.edges(data=True)
            sort_edges = sorted(edges_graph, key=lambda x: x[2]['weight'])

            new_graphs_deletes_edge = create_graphs_delete_edge(
                graph, best_solutions, sort_edges, proccess_data, original_prob)
            graph.evaluated = True

            graphs_evaluated.extend(new_graphs_deletes_edge)

        if len(best_solutions) > 0:
            best_value = float('inf')
            for graph in best_solutions:
                emd_value = graph.loss_value
                if emd_value < best_value:
                    best_value = emd_value
                    graph_solition = graph

            #is_solution = True

    return graph_solition

# Para cada grafo a evaluar, crea un nuevo grafo con la arista eliminada que este dentro de la cota
# Calcula su nueva probabilidad y valor de perdida, si el grafo deja de ser conexto
# es un grafo solucion y lo almacena en best_solutions, ademas cambia la cota de corte
# de ser conexo agrega el grafo a grafos por evaluar
def create_graphs_delete_edge(father_network: Graph, best_solutions: list, edges, proccess_data, original_prob):
    val_cup = proccess_data['val_cup']
    new_graphs = []
    emd_graph = father_network.loss_value

    for edge in edges:
        nodex, nodey, details = edge
        base_value, max_value = calcule_posible_emd(
            father_network.removed_edges, edge, emd_graph)

        if base_value < proccess_data['val_cup']:
            new_graph = remove_edges.create_new_graph(father_network, edge)
            new_graph.removed_edges.extend(father_network.removed_edges)

            remove_edges.calcule_probability_dist(
                new_graph, father_network.table_probability, proccess_data)
            new_emd = emd.calcule_emd(
                new_graph, proccess_data['state'], original_prob)
            print(f'Edge: {edge} - Value: {base_value}')
            print(f'Base emd: {base_value} - cut value: {proccess_data['val_cup']}')
            print(f'New emd: {new_emd}')
            print(f'Base emd: {base_value} - Max emd: {max_value}')
            print(f'Edges: {new_graph.edges(data=True)}')
            print(f'EdgesRemoved: {new_graph.removed_edges}')
            print(f'Is connected: {nx.is_connected(new_graph)}\n')

            new_graph.loss_value = new_emd
            modify_tables = {key.replace(
                "'", ""): value for key, value in new_graph.table_probability.items()}
            new_graph.table_probability = modify_tables

            if not nx.is_connected(new_graph):
                proccess_data['val_cup'] = new_emd
                best_solutions.append(new_graph)

            else:
                if new_emd <= proccess_data['val_cup']:
                    new_graphs.append(new_graph)

    return new_graphs


def calcule_posible_emd(removed_edges, new_edge, emd_graph):
    group_nodes = {}
    no_zero_edges = [edge for edge in removed_edges if edge[2] != 0.0]
    no_zero_edges.append(new_edge)

    if len(no_zero_edges) == 0:
        return emd_graph + new_edge[2]['weight']

    for edge in no_zero_edges:
        node1, node2, details = edge
        destino, origen = utils.get_type_nodes(node1, node2)
        
        if destino not in group_nodes:
            group_nodes[destino] = {}
            
        group_nodes[destino]["base"] = details['weight'] if details['weight'] > group_nodes[destino].get(
            "base", 0) else group_nodes[destino].get("base", 0)
        group_nodes[destino]["sum"] = group_nodes[destino].get(
            "sum", 0) + details['weight']
        
    
    base_values = round(sum(value['base'] for value in group_nodes.values()), 2) 
    sum_values = sum(value['sum'] for value in group_nodes.values())

    return base_values, sum_values



# Cota inicial de corte
def calcule_cut_value(network: Graph, num_channels_current):
    sum_val_emd = 0

    for edge in network.edges(data=True):
        _, _, details_edge = edge
        weight = details_edge['weight']

        sum_val_emd += weight

    value_cup = (sum_val_emd / len(network.edges())) * num_channels_current

    return round(value_cup, 3)
