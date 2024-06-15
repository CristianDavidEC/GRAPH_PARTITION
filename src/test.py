import pandas as pd

def get_marginalize_channel(tabla_marg, current_channels, all_channels='ABC'):
    table_prob = tabla_marg
    table_prob['state'] = tabla_marg.index
    new_channels = all_channels

    for channel in all_channels:
        if channel not in current_channels:
            #print(channel)
            table_prob, new_channels = marginalize_table(
                table_prob, channel, new_channels)
            
    
    table_prob = table_prob.reset_index().set_index('state')
    table_prob.index.name = None
    table_prob = table_prob.drop('index', axis=1)
    
    return table_prob


def marginalize_table(table, channel, channels='ABC'):
    position_element = channels.find(channel)
    table['state'] = table['state'].apply(modify_state, element=position_element)
    promd_table = table.groupby('state').mean()
    promd_table = promd_table.reset_index()
    new_channels = change_channels(channel, channels)

    return promd_table, new_channels
    
def modify_state(state, element):
    state = list(state)
    del state[element]

    return ''.join(state)


def change_channels(channel, channels='ABC'):
    element = channels.find(channel)
    if element != -1:
        return channels[:element] + channels[element + 1:]

    return channels

# Ejemplo malo !!!!
# # Creación del DataFrame de prueba
# data = {
#     '00': [1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
#     '01': [0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0],
#     '10': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
#     '11': [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0]
# }
# index = ['000', '001', '010', '011', '100', '101', '110', '111']
# df = pd.DataFrame(data, index=index)

# # Ejecución de la función
# result = get_marginalize_channel(df, 'A', 'ABC')


#Ejemplo bueno !!!
data = {
    '000': [0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    '001': [0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0],
    '010': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    '011': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    '100': [0.5, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
    '101': [0.0, 0.0, 1.0, 0.0, 0.5, 0.0, 0.0, 0.0],
    '110': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
    '111': [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
}

index = ['000', '001', '010', '011', '100', '101', '110', '111']

df = pd.DataFrame(data, index=index)


result = get_marginalize_channel(df, 'ABC', 'ABC')
print(result)


# # Ejemplo XX !!!
# data = {
#     '00': [1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
#     '01': [0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0],
#     '10': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
#     '11': [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0]
# }

# index = ['000', '001', '010', '011', '100', '101', '110', '111']

# df = pd.DataFrame(data, index=index)


# result = get_marginalize_channel(df, 'C', 'BC')
# print(result)