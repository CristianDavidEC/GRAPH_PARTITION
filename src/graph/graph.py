import networkx as nx
from itertools import product

class Graph(nx.Graph):
    def __init__(self):
        super().__init__()

    def create_graph(self, nodes):
        new_edges = self.create_edges(nodes)
        self.add_edges_from(new_edges)

        return self

    def create_edges(self, current_nodes):
        current_nodes = list(current_nodes)
        future_nodes = [f_node + "'" for f_node in current_nodes]

        edges = list(product(current_nodes, future_nodes))

        return edges
        
