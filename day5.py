# -*- coding: utf-8 -*-

def get_id(code):
    ftb = code[:7]
    ltr = code[7:]
    row, column = 0, 0
    for i in range(7):
        row += (2**(6-i))*(ftb[i] == 'B')
    for k in range(3):
        column += (2**(2-k))*(ltr[k] == 'R')
    return 8*row + column


def find_missing(ids):
    ids = sorted(ids)
    for i in range(len(ids)):
        if ids[i] - ids[i-1] == 2:
            return(ids[i]-1)


def masterfunc(line_list, part):
    if part == 1:
        return max([get_id(line) for line in line_list])
    if part == 2:
        return find_missing([get_id(line) for line in line_list])


def test(day, targetvals):
    with open("day" + str(day) + "_test.txt") as input_file:
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
    day = 5
    testvals = [820, None]
    if test(day, testvals):
        with open("day" + str(day) + "_input.txt") as input_file:
            read_data = input_file.read()
            line_list = read_data.split('\n')
        for i, _ in enumerate(testvals):
            output = masterfunc(line_list, i+1)
            print(f'Part {i+1}: {output}')
