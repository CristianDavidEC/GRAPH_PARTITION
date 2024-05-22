import threading
from graph.graph import Graph
import networkx as nx
#from marginalize import 

def remove_edges(network: Graph, probabilities, proccess_data):
    for removed_edge in network.edges():
        original_graph = network.copy()
        original_graph.remove_edge(*removed_edge)

        graph_processor = Graph()
        graph_processor.add_edges_to_graph(original_graph.edges())

        prob_expression = graph_processor.conver_edges_to_probability_expression()

        if nx.is_connected(graph_processor):
            print('Graph is connected')
        
        else:
            pass


def calcule_probabilities_connect_graph(graph: Graph, probabilities, proccess_data):
    prob_expression = graph.conver_edges_to_probability_expression()

    for future, current in prob_expression.items():
        proccess_data['future'] = future.replace("'", "")
        proccess_data['current'] = current
        





