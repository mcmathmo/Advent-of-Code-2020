from time import perf_counter
import numpy as np
from numpy.linalg import matrix_power as matpow


class ship:
    def __init__(self):
        self.pos = np.array((0, 0))
        self.dir = np.array((1, 0))
        self.R = np.array([[0, -1], [1, 0]])

    def move(self, instruction):
        char = instruction[0]
        mag = int(instruction[1:])
        if char == 'N':
            self.pos += (0, mag)
        elif char == 'S':
            self.pos += (0, -mag)
        elif char == 'E':
            self.pos += (mag, 0)
        elif char == 'W':
            self.pos += (-mag, 0)
        elif char == 'F':
            self.pos += mag*self.dir
        elif char == 'L':
            self.dir = np.matmul(matpow(self.R, int(mag/90)), self.dir)
        elif char == 'R':
            self.dir = np.matmul(matpow(-self.R, int(mag/90)), self.dir)


class wayship:
    def __init__(self):
        self.pos = np.array((0, 0))
        self.waypos = np.array((10, 1))
        self.R = np.array([[0, -1], [1, 0]])

    def move(self, instruction):
        char = instruction[0]
        mag = int(instruction[1:])
        if char == 'N':
            self.waypos += (0, mag)
        elif char == 'S':
            self.waypos += (0, -mag)
        elif char == 'E':
            self.waypos += (mag, 0)
        elif char == 'W':
            self.waypos += (-mag, 0)
        elif char == 'F':
            self.pos += mag*self.waypos
        elif char == 'L':
            self.waypos = np.matmul(matpow(self.R, int(mag/90)), self.waypos)
        elif char == 'R':
            self.waypos = np.matmul(matpow(-self.R, int(mag/90)), self.waypos)


def ship_distance(line_list):
    myship = ship()
    for line in line_list:
        myship.move(line)
    return np.sum(np.absolute(myship.pos))


def wayship_distance(line_list):
    myship = wayship()
    for line in line_list:
        myship.move(line)
    return np.sum(np.absolute(myship.pos))


def get_result(line_list, part):
    if part == 1:
        return ship_distance(line_list)
    elif part == 2:
        return wayship_distance(line_list)


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
    day = 12
    testvals = [25, 286]
    main()
