from execute import execute

if __name__ == '__main__':
    data_to_process = {
        'file': 'data/tablex6-ramdom.json',
        'future': 'ABC',
        'current': 'ABCD',
        'state': '1101',
        'channels': 'ABCDEF',
        'method': 'partition' # partition | delete_edges
    }

    execute(data_to_process)
