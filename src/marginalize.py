import pandas as pd

def get_marginalize_channel(tabla_marg, current_channels, all_channels='ABC'):
    table_prob = tabla_marg
    new_channels = all_channels

    for channel in all_channels:
        if channel not in current_channels:
            table_prob, new_channels = marginalize_table(
                table_prob, channel, new_channels)

    return table_prob


def marginalize_table(table, channel, channels='ABC'):
    df_group = table.groupby(group_index(
        table.index, channel, channels)).mean()
    new_channels = change_channels(channel, channels)
    
    return df_group, new_channels


def group_index(indexes, channel, channels='ABC'):
    element = channels.find(channel)
    if element != -1:
        return [modify_index(index, element) for index in indexes]

    return indexes
    
def modify_index(index, element):
    return index[:element] + index[element + 1:]


def change_channels(channel, channels='ABC'):
    element = channels.find(channel)
    if element != -1:
        return channels[:element] + channels[element + 1:]

    return channels
