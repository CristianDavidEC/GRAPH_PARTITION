from main_partition import main_partition
from main_delete_edge import main_delete_edge

if __name__ == '__main__':
    data_to_process = {
        'file': 'data/tablex5.json',
        'future': 'ABCDE',
        'current': 'ABCDE',
        'state': '10001',
        'channels': 'ABCDE',
        'method': 'partition' # partition | delete_edges |
    }

    if data_to_process['method'] == 'partition':
        main_partition(data_to_process)
    
    if data_to_process['method'] == 'delete_edges':
        main_delete_edge(data_to_process)