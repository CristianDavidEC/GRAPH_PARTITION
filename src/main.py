from execute import execute

if __name__ == '__main__':
    data_to_process = {
        'file': 'data/testx8.json',
        'future': 'ABCDEFGH',
        'current': 'ABCDEFGH',
        'state': '11011110',
        'channels': 'ABCDEFGH',
        'method': 'delete_edges' # partition | delete_edges
    }

    execute(data_to_process)
