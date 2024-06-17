from execute import execute

if __name__ == '__main__':
    data_to_process = {
        'file': 'data/tablex5.json',
        'future': 'ABCDE',
        'current': 'ABCD',
        'state': '1111',
        'channels': 'ABCDE',
        'method': 'partition' # partition | delete_edges
    }

    execute(data_to_process)
