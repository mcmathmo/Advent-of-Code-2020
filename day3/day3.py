# -*- coding: utf-8 -*-

from math import prod

def traverse_slope(slope, xstepsize, ystepsize):
    xloc, yloc = 0, 0
    height = len(slope)
    width = len(slope[0])
    trees_hit = 0
    while yloc < height:
        if slope[yloc][xloc] == '#':
            trees_hit += 1
        yloc += ystepsize
        xloc = (xloc + xstepsize) % width
    return trees_hit


def masterfunc(line_list, part):
    if part == 1:
        return traverse_slope(line_list, 3, 1)
    if part == 2:
        grads = ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2))
        return prod([traverse_slope(line_list, *grad) for grad in grads])


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
    day = 3
    testvals = [7, 336]
    if test(day, testvals):
        with open("day" + str(day) + "_input.txt") as input_file:
            read_data = input_file.read()
            line_list = read_data.split('\n')
        for i, _ in enumerate(testvals):
            output = masterfunc(line_list, i+1)
            print(f'Part {i+1}: {output}')
