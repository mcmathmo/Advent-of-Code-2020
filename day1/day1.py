# -*- coding: utf-8 -*-

def two_sum(vals, target):
    complement_dict = dict()
    for val in vals:
        if val in complement_dict:
            return val, complement_dict[val]
        else:
            complement_dict[target-val] = val
    return False


def three_sum(vals, target):
    for index, val in enumerate(vals):
        state = two_sum(vals[index:], target-val)
        if state:
            return val, state[0], state[1]


if __name__ == "__main__":
    input_file = open("day1_input.txt")
    read_data = input_file.read()
    strings_split = read_data.split()
    inputs = [int(x) for x in strings_split]
    val1, val2, val3 = three_sum(inputs, 2020)
    print(val1*val2*val3)