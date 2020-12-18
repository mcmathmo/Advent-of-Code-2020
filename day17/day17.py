from time import perf_counter
import numpy as np
from itertools import product


class ConwayCube:
    def __init__(self, initstate, maxsteps, dimension):
        offset = maxsteps + 1
        maxlength = len(initstate[0]) + 2*offset
        self.cube = np.zeros((maxlength,)*dimension)
        for x, line in enumerate(initstate):
            for y, char in enumerate(line):
                loc = [x+offset, y+offset] + [offset]*(dimension-2)
                self.cube[tuple(loc)] = int(char == '#')
        self.offset = offset
        rng = range(-1, 2)
        self.veclist = [np.array(vec) for vec in product(*(rng,)*dimension)
                        if vec != (0,)*dimension]
        self.cstep = 1
        self.dimension = dimension

    def countneighbours(self, pos):
        tot = 0
        for vec in self.veclist:
            if self.cube[tuple(pos+vec)]:
                tot += 1
                if tot == 4:
                    return 4
        return tot

    def step(self):
        rng = range(-self.cstep, len(self.cube) - self.offset + self.cstep)
        cubecopy = np.copy(self.cube)
        for cellpos in product(*(rng,)*self.dimension):
            neighbours = self.countneighbours(np.array(cellpos))
            if self.cube[cellpos] and neighbours not in {2.0, 3.0}:
                cubecopy[cellpos] = 0
            elif (not self.cube[cellpos]) and neighbours == 3.0:
                cubecopy[cellpos] = 1
        self.cube = cubecopy
        self.cstep += 1
        return self

    def total_active(self):
        rng = range(len(self.cube))
        return sum((self.cube[pos] for pos in product(*(rng,)*self.dimension)))


def game_of_life(line_list, steps, dimension):
    conway = ConwayCube(line_list, steps, dimension)
    for _ in range(steps):
        conway.step()
    return conway.total_active()


def get_result(line_list, part):
    if part == 1:
        return game_of_life(line_list, 6, 3)
    elif part == 2:
        return game_of_life(line_list, 6, 4)


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
    day = 17
    testvals = [112, 848]
    main()
