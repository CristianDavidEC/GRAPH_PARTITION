from execute import execute

if __name__ == '__main__':
    data_to_process = {
        'file': 'data/tablex3.json',
        'future': 'ABC',
        'current': 'ABC',
        'state': '111',
        'channels': 'ABC',
        'method': 'delete_edges' # partition | delete_edges
    }

    execute(data_to_process)
