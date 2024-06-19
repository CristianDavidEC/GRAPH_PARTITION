from execute import execute

if __name__ == '__main__':
    data_to_process = {
        'file': 'test/files/red_10.json',
        'future': 'ABC',
        'current': 'ABCD',
        'state': '1000',
        'channels': 'ABCDEFGHIJ', # 10000000
        'method': 'partition' # partition | delete_edges
    }

    execute(data_to_process)