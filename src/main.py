from execute import execute

if __name__ == '__main__':
    data_to_process = {
        'file': 'data/tablex5.json',
        'future': 'ABC',
        'current': 'ABC',
        'state': '100', #10001
        'channels': 'ABCDE',
        'method': 'delete_edges' # partition | delete_edges
    }

    execute(data_to_process)
