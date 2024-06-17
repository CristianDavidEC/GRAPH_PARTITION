from execute import execute

if __name__ == '__main__':
    data_to_process = {
        'file': 'data/tablex5.json',
        'future': 'ABCDEF',
        'current': 'ABCD',
        'state': '1111',
        'channels': 'ABCDEF',
        'method': 'delete_edges' # partition | delete_edges
    }

    execute(data_to_process)
