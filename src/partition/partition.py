import pandas as pd
import probability.probability as prob


def calculate_partition(process_data):
    combinations_current = find_combinations(process_data['current'])
    combinations_future = find_combinations(process_data['future'])

    table_comb = pd.DataFrame(
        index=combinations_current, columns=combinations_future)
    table_comb.fillna(-1)

    calcule_probability_partition(
        combinations_current, combinations_future, table_comb, process_data)


def calcule_probability_partition(currents, futures, table_comb, process_data):
    probabilities = prob.create_probability_distributions(process_data['file'])

    channels_current = process_data['current']
    channels_future = process_data['future']

    add_special_case(channels_current, channels_future, table_comb)

    print(table_comb)

    for current in currents:
        for future in futures:
            part_left, part_right = get_partition_exp(
                current, future, channels_current, channels_future)

            print(f'{part_left[0]}| {part_left[1]} x {
                  part_right[0]} | {part_right[1]}')

        if (table_comb != -1).all().all():
            break
    pass


# Special case to keys "" | "" x "ABC" | "ABC"
def add_special_case(channels_current, channels_future, table_comb):
    table_comb.loc[channels_current, channels_future] = 0
    table_comb.loc["", ""] = 0


def is_prob_table_complete(table):
    return table.isnull().all().all()


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
