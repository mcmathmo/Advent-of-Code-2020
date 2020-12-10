import numpy as np
from time import perf_counter


def joltage(intlist):
    diffs = np.append(np.diff(intlist),[3])
    sol = sum(diffs == 1) * (sum(diffs == 3))
    return sol, diffs


def arrangements(diffs):
    dplist = [1 for _ in diffs]
    rdiffs = diffs[::-1]
    dplist[2] = 2 if sum(rdiffs[1:3]) <= 3 else 1
    for i in range(3,len(rdiffs)):
        if sum(rdiffs[i-2:i+1]) == 3:
            dplist[i] = sum(dplist[i-3:i])
        elif sum(rdiffs[i-1:i+1]) <= 3:
            dplist[i] = sum(dplist[i-2:i])
        else:
            dplist[i] = dplist[i-1]
    return dplist[-1]


def get_result(line_list, part):
    intlist = [0] + [int(line) for line in line_list]
    intlist.sort()
    if part == 1:
        return joltage(intlist)[0]
    if part == 2:
        return arrangements(joltage(intlist)[1])


def test(day, targetvals):
    # Open test data, split by line
    with open("day" + str(day) + "_test.txt") as input_file:
        read_data = input_file.read()
        line_list = read_data.split('\n')
    resultvals = [0 for _ in range(len(targetvals))]
    for i, _ in enumerate(targetvals):
        resultvals[i] = get_result(line_list, i + 1)
        if resultvals[i] != testvals[i]:
            print(f'Test part {i+1} fails: expected '
                  f'{testvals[i]} but got {resultvals[i]}')
    return resultvals == testvals


def main():
    # Only run functions on the input if tests pass
    if test(day, testvals):
        # Open input data, split by line
        with open("day" + str(day) + "_input.txt") as input_file:
            read_data = input_file.read()
            line_list = read_data.split('\n')
        for i, _ in enumerate(testvals):
            tic = perf_counter()
            output = get_result(line_list, i + 1)
            toc = perf_counter()
            print(f'Part {i+1}: {output}')
            print(f'This took {toc-tic:0.7f} seconds')


if __name__ == "__main__":
    day = 10
    testvals = [220, 19208]
    main()
