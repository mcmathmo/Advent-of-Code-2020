from time import perf_counter
from math import prod


def modbus(notes):
    stime = int(notes[0])
    # Wait time = (-start_time) modulo initial_time
    return prod(min((-stime % int(bus), int(bus))
                    for bus in notes[1].split(',')
                    if bus != 'x'))


def CRTbus(notes):
    blist = [(-int(offset) % int(bus), int(bus))
             for offset, bus in enumerate(notes[1].split(','))
             if bus != 'x']
    # Uses the chinese remainder theorem to solve the simultaneous congruences
    N = prod((ni for ai, ni in blist))
    return sum((N*ai*pow(N//ni, -1, ni)//ni for ai, ni in blist)) % N


def get_result(line_list, part):
    if part == 1:
        return modbus(line_list)
    elif part == 2:
        return CRTbus(line_list)


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
    day = 13
    testvals = [295, 1068781]
    main()
