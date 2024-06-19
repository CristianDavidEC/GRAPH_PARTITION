from execute import execute

if __name__ == '__main__':
    data_to_process = {
        'file': 'data/tablex6-ramdom.json',
        'future': 'ABCD',
        'current': 'ABCD',
        'state': '1001',
        'channels': 'ABCDEF',#100010
        'method': 'delete_edges' # partition | delete_edges
    }

    execute(data_to_process)

