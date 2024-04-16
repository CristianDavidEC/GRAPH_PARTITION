import pandas as pd

def create_sub_table(data_frame, colum_extract):
    if colum_extract == '':
        return data_frame
    
    new_table = data_frame[[colum_extract]].copy()
    new_colum = colum_extract + '0'
    new_table.insert(0, new_colum, 1 - data_frame[colum_extract])

    return new_table