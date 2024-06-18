from itertools import product
from scipy.spatial.distance import cdist
from graph.graph import Graph
import probability.probability as prob
from pyemd import emd
import numpy as np
import pandas as pd

### Optiene el valor de EMD entre las dos distribuciones de probabilidad
### la libreria pyemd, utiliza las dos distribuciones de probabilidad
### y una matriz de distancia hamming de los estados de cada distribucion
def calcule_emd(graph: Graph, state, original_probability):
    modofy_prob = get_probability_in_state(graph, state)
    haming_matrix = hamming_distance_matrix(modofy_prob['state'].values)

    list_modofy_prob = modofy_prob['probability'].values
    list_original_prob = original_probability.loc[state].to_numpy()

    list_modofy_prob = np.ascontiguousarray(list_modofy_prob, dtype=np.double)
    list_original_prob = np.ascontiguousarray(
        list_original_prob, dtype=np.double)

    emd_value = emd(list_modofy_prob, list_original_prob, haming_matrix)

    return round(emd_value, 3)


### Calcula la probabilidad de un estado, en cada una de las distribuciones de probabilidad
### se une en una sola distribucion mediante el producto tensor
def get_probability_in_state(graph: Graph, state):
    table_probability = graph.table_probability
    prob_state = {}
    for future, table in table_probability.items():
        if isinstance(table, np.ndarray):
            prob_state[future] = table
            continue
        if state in table.index:
            prob_state[future] = table.loc[state].values

    probabiliry_result = prob.calculate_joint_probability(prob_state)

    return probabiliry_result


### Calcula la matrix de distancia hamming a partir de una matris de 
### estados dada.
def hamming_distance_matrix(states):
    state = list(map(lambda x: list(map(int, x)), states))
    haming_matrix = cdist(state, state, 'hamming') * len(state[0])

    return haming_matrix


### Calcula la distacia de emd entre dos distribuciones de probabilidad para el metodo de particionamiento.
def emd_partition(probability_table, original_probability, state):
    list_index = list(original_probability.columns)
    order_table = sorter_dataframe(probability_table, list_index)
    haming_matrix = hamming_distance_matrix(order_table['state'].values)

    list_modofy_prob = order_table['probability'].values
    list_original_prob = original_probability.loc[state].to_numpy()

    list_modofy_prob = np.ascontiguousarray(list_modofy_prob, dtype=np.double)
    list_original_prob = np.ascontiguousarray(
        list_original_prob, dtype=np.double)

    emd_value = emd(list_modofy_prob, list_original_prob, haming_matrix)

    return emd_value


def sorter_dataframe(dataframe, list_order):
    dataframe['order'] = pd.Categorical(
        dataframe['state'], categories=list_order, ordered=True
    )
    new_df = dataframe.sort_values('order').drop(columns='order')

    return new_df