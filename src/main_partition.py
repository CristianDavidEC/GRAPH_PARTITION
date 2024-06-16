import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import probability.utils as utils
import partition.partition as partition
from graph.graph import Graph
from graph.remove_edges import remove_edges


def main(process_data):
    partition.calculate_partition(process_data)
    
if __name__ == '__main__':
    data_to_process = {
        #'file': 'src/data/tablex5.json',
        'file': 'data/tablex5.json',
        'future': 'ABC',
        'current': 'AC',
        'state': '10',
        'channels': 'ABCDE',
        #'method': 'partition' # partition | delete_edges | clear_zeros | heuristicas
    }

    main(data_to_process)


