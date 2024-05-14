import threading
import networkx as nx

def remove_edges(network: nx.Graph, probabilities):
    for edge in network.edges():
        network.remove_edge(edge[0], edge[1])
        
