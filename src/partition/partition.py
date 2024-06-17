import pandas as pd
import probability.probability as prob
import probability.utils as utils
import time as t
import emd.emd_calculation as emd


# Inicializa la tabla de combinaciones y calcula las combinaciones de current y future
def calculate_partition(process_data):
    combinations_current = find_combinations(process_data['current'])
    combinations_future = find_combinations(process_data['future'])

    dic_combinations = create_table_combination(
        combinations_future, combinations_current)

    result_partition = calcule_probability_partition(
        combinations_current, combinations_future, dic_combinations, process_data)

    return result_partition
    

# Calcula la mejor particion posible de los elementos, dadas las combinaciones de current y future
# combina la union de los dos en una particion y la otra particion es el complemento de estos dos
# mientras se van realizando los calculos el valor de las tablas encontradas se almacena en una tabla mara reusarlas
# @ currents: combinaciones de current
# @ futures: combinaciones de future
# @ dic_combinations: diccionario con las tablas de probabilidad
# @ process_data: diccionario con los datos del proceso
def calcule_probability_partition(currents, futures, dic_combinations, process_data):
    probabilities = utils.create_probability_distributions(
        process_data['file'])
    original_prob = prob.original_probability_partition(
        probabilities, process_data['current'], process_data['future'], process_data['channels'])

    channels_current = process_data['current']
    channels_future = process_data['future']
    process_data['original_channels'] = channels_current
    best_partition = {
        'partition': None,
        'value': float('inf')
    }

    for current in currents:
        if all(bool(valor) for valor in dic_combinations.values()):
            break
        for future in futures:
            parts = get_partition_exp(
                current, future, channels_current, channels_future)
            part_left, part_right = parts
            partition_left_tab = calculate_parts(
                part_left, dic_combinations, probabilities, process_data, original_prob)
            partition_right_tab = calculate_parts(
                part_right, dic_combinations, probabilities, process_data, original_prob)
            result_emd, tensor_product = calcule_emd_partitions(
                partition_left_tab, partition_right_tab, original_prob, parts, process_data['state'])
                
            # Particion de perdida 0, mejor particion
            if result_emd == 0:
                best_partition['partition'] = parts
                best_partition['value'] = result_emd
                best_partition['tensor_product'] = tensor_product

                return best_partition

            if result_emd < best_partition['value']:
                best_partition['partition'] = parts
                best_partition['value'] = result_emd
                best_partition['tensor_product'] = tensor_product

    return best_partition

# Calcula las tablas y probabilidad de cada una de las subpartes que componen la particion
# @ return: tabla de probabilidad de la paricion
def calculate_parts(partition, dic_combinations, probabilities, process_data, original_prob):
    furure, current = partition
    table_prob_partition = None
    key_comb = furure+'|'+current

    if dic_combinations[key_comb]:
        table_prob_partition = dic_combinations[key_comb]
    else:
        if furure == '' and current == '':
            dic_combinations[key_comb] = -1
            return

        state = get_value_state(
            current, process_data['current'], process_data['state'])

        data_to_process = {
            'future': furure,
            'current': current,
            'state': state,
            'channels': process_data['channels'],
            'original_channels': process_data['original_channels'],
        }

        table_prob_partition = prob.get_probability_tables_partition(
            data_to_process, probabilities, dic_combinations, original_prob)

    prob_result = prob.calculate_joint_probability(table_prob_partition)

    return prob_result

# Calcula la perdida de la particion
def calcule_emd_partitions(partition_left, partition_right, original_prob, parts_exp, state):
    if partition_left is None or partition_right is None:
        return 10000, None
    
    tensor_product = prob.tensor_product_partition(
        partition_left, partition_right, parts_exp)
    
    value_emd = emd.emd_partition(tensor_product, original_prob, state)

    return value_emd, tensor_product


def get_value_state(current, all_current, state):
    val_state = ''
    for l in current:
        position = all_current.find(l)
        if position != -1:
            val_state += state[position]

    return val_state


def is_valid_partition(part_left, part_right):
    if part_left[0] == "" and part_left[1] == "":
        return False
    if part_right[0] == "" and part_right[1] == "":
        return False

    return True

# A partir del current y future calcula su particion complementaria	
def get_partition_exp(current, future, channels_current, channels_future):
    current_comple = missing_elements(current, channels_current)
    future_comple = missing_elements(future, channels_future)

    part_left = (future, current)
    part_right = (future_comple, current_comple)

    return part_left, part_right


def missing_elements(input, original):
    set_original = set(original)
    set_input = set(input)

    missing = set_original - set_input
    missing = "".join(sorted(missing))

    return missing


# Dada la lista de canales calcula las combinaciones posibles de sus elementos
def find_combinations(s):
    def backtrack(start, path, length):
        if len(path) == length:
            combinations.append(''.join(path))
            return
        for i in range(start, len(s)):
            path.append(s[i])
            backtrack(i + 1, path, length)
            path.pop()
    combinations = []
    for length in range(1, len(s) + 1):
        backtrack(0, [], length)

    combinations.insert(0, '')
    return combinations


# Tabla auxiliar para almacenar las tablas de probabilidad calculadas previamente
def create_table_combination(future, current):
    combinations = [str(x) + '|' + str(y) for x in future for y in current]

    dic_combinations = dict.fromkeys(combinations, {})

    return dic_combinations
