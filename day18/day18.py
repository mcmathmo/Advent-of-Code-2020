from time import perf_counter


def find_obracket(string):
    opensofar = 0
    for idx, char in enumerate(string):
        if char == ')':
            opensofar += 1
        elif char == '(':
            opensofar -= 1
            if opensofar == 0:
                return idx


def find_cbracket(string):
    opensofar = 0
    for idx, char in enumerate(string):
        if char == '(':
            opensofar += 1
        elif char == ')':
            opensofar -= 1
            if opensofar == 0:
                return idx


def lparse(line):
    if len(line) == 1:
        return int(line[0])
    if line[0] == ')':
        # if start with bracket solve bracket first
        idx = find_obracket(line)
        return lparse([lparse(line[1:idx])] + line[idx+1:])
    else:
        if line[2] == ')':
            idx = find_obracket(line)
            return lparse(line[:2] + [lparse(line[3:idx])] + line[idx+1:])
        else:
            leftint = int(line[0])
            if line[1] == '+':
                return leftint + lparse(line[2:])
            else:
                return leftint * lparse(line[2:])


def sum_lparsed(line_list):
    return sum((lparse([i for i in ''.join(line.split())[::-1]])
               for line in line_list))


def sum_bparsed(line_list):
    return sum((bparse([i for i in ''.join(line.split())])
               for line in line_list))


def bparse(line):
    if len(line) == 1:
        return int(line[0])
    for idx, val in enumerate(line):
        if val == '(':
            cidx = find_cbracket(line)
            return bparse(line[:idx] + [bparse(line[idx+1:cidx])] + line[cidx+1:])
    for idx, val in enumerate(line):
        if val == '*':
            return bparse([bparse(line[:idx]) * bparse(line[idx+1:])])
    for idx, val in enumerate(line):
        if val == '+':
            return bparse([bparse(line[:idx]) + bparse(line[idx+1:])])


def get_result(line_list, part):
    if part == 1:
        return sum_lparsed(line_list)
    elif part == 2:
        return sum_bparsed(line_list)


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
    day = 18
    testvals = [26335, 693891]
    main()
