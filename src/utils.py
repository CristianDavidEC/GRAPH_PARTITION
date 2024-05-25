import pandas as pd
import json

def create_sub_table(data_frame, colum_extract):
    if colum_extract == '':
        return data_frame
    
    new_table = data_frame[[colum_extract]].copy()
    new_colum = colum_extract + '0'
    new_table.insert(0, new_colum, 1 - data_frame[colum_extract])

    return new_table

def create_probability_distributions(json_file):
    probability_distributions = {}
    with open(json_file, 'r') as archivo:
        datos = json.load(archivo)

    for channel, dist_prob in datos.items():
        probability_distributions[channel] = pd.DataFrame(dist_prob).T

    
    return probability_distributions

def get_type_nodes(node1, node2):
    if "'" in node1:
        return node1, node2
    
    return node2, node1