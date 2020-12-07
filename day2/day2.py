# -*- coding: utf-8 -*-


from collections import Counter


def rule_one_satisfy(line):
    firstindex = line.index('-')
    secondindex = line.index(' ')
    minval = int(line[:firstindex])
    maxval = int(line[firstindex+1:secondindex])
    letter = line[secondindex+1]
    password = line[secondindex+4:]
    charcounts = Counter(password)
    charval = charcounts[letter]
    return charval >= minval and charval <= maxval


def rule_two_satisfy(line):
    firstindex = line.index('-')
    secondindex = line.index(' ')
    loc_one = int(line[:firstindex]) - 1
    loc_two = int(line[firstindex+1:secondindex]) - 1
    letter = line[secondindex+1]
    password = line[secondindex+4:]
    return sum([letter == password[loc] for loc in [loc_one, loc_two]]) == 1


def masterfunc(line_list, part):
    if part == 1:
        return sum([1 for line in line_list if rule_one_satisfy(line)])
    elif part == 2:
        return sum([1 for line in line_list if rule_two_satisfy(line)])


def test(day, targetvals):
    input_file = open("day" + str(day) + "_test.txt")
    read_data = input_file.read()
    line_list = read_data.split('\n')
    resultvals = [0 for _ in range(len(targetvals))]
    for i, _ in enumerate(targetvals):
        resultvals[i] = masterfunc(line_list, i+1)
        if resultvals[i] != testvals[i]:
            print(f'Test part {i+1} fails: expected '
                  f'{testvals[i]} but got {resultvals[i]}')
    return resultvals == testvals


if __name__ == "__main__":
    day = 2
    testvals = [2, 1]
    if test(day, testvals):
        input_file = open("day" + str(day) + "_input.txt")
        read_data = input_file.read()
        line_list = read_data.split('\n')
        for i, _ in enumerate(testvals):
            output = masterfunc(line_list, i+1)
            print(f'Part {i+1}: {output}')
