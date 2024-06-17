from main_partition import main_partition
from main_delete_edge import main_delete_edge

def execute(data_to_process):
    if data_to_process['method'] == 'partition':
        main_partition(data_to_process)

    if data_to_process['method'] == 'delete_edges':
        main_delete_edge(data_to_process)