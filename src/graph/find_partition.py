from graph.graph import Graph
import emd.emd_calculation as emd
import graph.remove_edges as remove_edges

def find_best_partition(network: Graph, proccess_data, original_prob):
    val_cup = calcule_cut_value(network)
    proccess_data['channels'] = proccess_data['current']
    proccess_data['val_cup'] = val_cup
    best_solutions = []
    graphs_evaluated = [network]
    graph_solition = None

    is_solution = False
    while not is_solution:
        graphs_sort = sorted(graphs_evaluated, key=lambda graph: (
            graph.loss_value, len(graph.removed_edges)), reverse=True)

        for graph in graphs_sort:
            if graph.evaluated:
                continue
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

            is_solution = True
    
    print(graph_solition.edges(data=True))
    print(graph_solition.loss_value)
    print(graph_solition.removed_edges)
    print(vars(graph_solition))


def create_graphs_delete_edge(father_network: Graph, best_solutions: list, edges, proccess_data, original_prob):
    val_cup = proccess_data['val_cup']
    new_graphs = []
    emd_graph = father_network.loss_value

    for edge in edges:
        nodex, nodey, details = edge
        possible_emd = emd_graph + details['weight']
        if possible_emd < val_cup:
            new_graph = remove_edges.create_new_graph(father_network, (nodex, nodey))
            remove_edges.calcule_probability_dist(
                new_graph, father_network.table_probability, proccess_data)

            new_emd = emd.calcule_emd(
                new_graph, proccess_data['state'], original_prob)

            new_graph.loss_value = new_emd
            modify_tables = {key.replace(
                "'", ""): value for key, value in new_graph.table_probability.items()}
            new_graph.table_probability = modify_tables

            if not nx.is_connected(new_graph):
                proccess_data['val_cup'] = new_emd
                best_solutions.append(new_graph)

            else:
                if new_emd <= val_cup:
                    new_graphs.append(new_graph)

    return new_graphs


def calcule_cut_value(network: Graph):
    sum_val_emd = 0

    for edge in network.edges(data=True):
        _, _, details_edge = edge
        weight = details_edge['weight']

        sum_val_emd += weight

    return sum_val_emd / 2
