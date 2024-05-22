import networkx as nx
from itertools import product

class Graph(nx.Graph):
    def __init__(self):
        super().__init__()

    def create_graph(self, nodes: str):
        new_edges = self.create_edges(nodes)
        self.add_edges_from(new_edges)

        return self

    def create_edges(self, current_nodes):
        current_nodes = list(current_nodes)
        future_nodes = [f_node + "'" for f_node in current_nodes]

        edges = list(product(current_nodes, future_nodes))

        return edges
    
    def add_edges_to_graph(self, edges: list):
        self.add_edges_from(edges)

    def conver_edges_to_probability_expression(self):
        exp_edges_prob = {}

        for edges in self.edges():
            node1, node2 = edges

            type_nodes= self._get_type_nodes(node1, node2)
            future = type_nodes['future']
            current = type_nodes['current']

            if future not in exp_edges_prob:
                exp_edges_prob[future] = ''

            exp_edges_prob[future] = exp_edges_prob[future] + current
        
        return exp_edges_prob

    # def add_disconnected_nodes(self, exp_edges_prob):
    #     for node in self.nodes():
    #         if node not in exp_edges_prob:
    #             if "'" in node:
    #                 exp_edges_prob[node] = ""
    #             else:
    #                 exp_edges_prob[""] = ""
    #                 exp_edges_prob[""] = exp_edges_prob[""] + node


    def _get_type_nodes(self, node1, node2):
        if "'" in node1:
            return {
                'future': node1,
                'current': node2
            }
        
        return {
            'future': node2,
            'current': node1
        }

