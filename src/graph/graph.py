import networkx as nx
from itertools import product

def create_graph(nodes):
    new_edges = create_edges(nodes)
    graph = nx.Graph()
    graph.add_edges_from(new_edges)

    return graph

def create_edges(current_nodes):
    current_nodes = list(current_nodes)
    future_nodes = [f_node + "'" for f_node in current_nodes]

    edges = list(product(current_nodes, future_nodes))

    return edges
    
