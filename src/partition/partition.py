import pandas as pd
import probability.probability as prob
import probability.utils as utils


def calculate_partition(process_data):
    combinations_current = find_combinations(process_data['current'])
    combinations_future = find_combinations(process_data['future'])

    dic_combinations = create_table_combination(
        combinations_current, combinations_future)

    calcule_probability_partition(
        combinations_current, combinations_future, dic_combinations, process_data)


def calcule_probability_partition(currents, futures, dic_combinations, process_data):
    probabilities = utils.create_probability_distributions(
        process_data['file'])

    original_prob = prob.original_probability_partition(
        probabilities, process_data['current'], process_data['future'], process_data['channels'])

    channels_current = process_data['current']
    channels_future = process_data['future']

    process_data['original_channels'] = channels_current
    

    for current in currents:
        for future in futures:
            part_left, part_right = get_partition_exp(
                current, future, channels_current, channels_future)

            if is_valid_partition(part_left, part_right):
                # print(f'{part_left[0]}|{part_left[1]} x {
                #     part_right[0]}|{part_right[1]}')
                partition_left_tab = calculate_parts(
                    part_left, dic_combinations, probabilities, process_data, original_prob)
                partition_right_tab = calculate_parts(
                    part_right, dic_combinations, probabilities, process_data, original_prob)
            else:
                calculate_parts(part_left, dic_combinations,
                                probabilities, process_data, original_prob)
                calculate_parts(part_right, dic_combinations,
                                probabilities, process_data, original_prob)

        if all(dic_combinations.values()):
            print('all combinations')
            break

    print(dic_combinations)


def calculate_parts(partition, dic_combinations, probabilities, process_data, original_prob):
    furure, current = partition
    table_prob_partition = None
    key_comb = current+'|'+furure

    if furure == '' and current == '':
        dic_combinations[key_comb] = 0
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

    # if dic_combinations[key_comb] is not None:
    #     table_prob_partition = dic_combinations[key_comb]

    table_prob_partition = prob.get_probability_tables_partition(
        data_to_process, probabilities, dic_combinations, original_prob)


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


# # Special case to keys "" | "" x "ABC" | "ABC"
# def add_special_case(channels_current, channels_future, table_comb):
#     table_comb.loc[channels_current, channels_future] = 0
#     table_comb.loc["", ""] = 0
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


# Get the combination to channels
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


def create_table_combination(future, current):
    combinations = [str(x) + '|' + str(y) for x in future for y in current]

    dic_combinations = dict.fromkeys(combinations, None)

    return dic_combinations
