from execute import execute

if __name__ == '__main__':
    data_to_process = {
        'file': 'data/sustentacion-8b.json',
        'future': 'ABCDEFGH',
        'current': 'ABCDEFGH',
        'state': '10000000',
        'channels': 'ABCDEFGH',
        'method': 'delete_edges' # partition | delete_edges
    }

    execute(data_to_process)
