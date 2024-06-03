from itertools import product
from scipy.spatial.distance import cdist
from graph.graph import Graph
import probability.probability as prob
from pyemd import emd
import numpy as np


def calcule_emd(graph: Graph, state, original_probability):
    modofy_prob = get_probability_in_state(graph, state)
    haming_matrix = hamming_distance_matrix(modofy_prob['state'].values)

    print('\nEMD Calculation')

    list_modofy_prob = modofy_prob['probability'].values
    list_original_prob = original_probability.loc[state].to_numpy()

    # print(f'List Modify Prob \n{list_modofy_prob}')
    # print(f'List Original Prob \n{list_original_prob}')
    # print(f'Haming Matrix \n{haming_matrix}')

    list_modofy_prob = np.ascontiguousarray(list_modofy_prob, dtype=np.double)
    list_original_prob = np.ascontiguousarray(
        list_original_prob, dtype=np.double)

    emd_value = emd(list_modofy_prob, list_original_prob, haming_matrix)

    return emd_value


def get_probability_in_state(graph: Graph, state):
    table_probability = graph.table_probability
    prob_state = {}
    for future, table in table_probability.items():
        if state in table.index:
            prob_state[future] = table.loc[state].values

    probabiliry_result = prob.calculate_joint_probability(prob_state)

    return probabiliry_result


def hamming_distance_matrix(states):
    state = list(map(lambda x: list(map(int, x)), states))
    haming_matrix = cdist(state, state, 'hamming') * len(state[0])

    return haming_matrix
