from execute import execute

if __name__ == '__main__':
    data_to_process = {
        'file': 'test/files/tablex5.json',
        'future': 'ABC',
        'current': 'ABC',
        'state': '100',
        'channels': 'ABCDEFGH',#10000000
        'method': 'delete_edges' # partition | delete_edges
    }

    execute(data_to_process)