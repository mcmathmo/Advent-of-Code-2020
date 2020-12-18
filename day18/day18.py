from time import perf_counter


def find_cbracket(string):
    opensofar = 0
    for idx, char in enumerate(string):
        if char == '(':
            opensofar += 1
        elif char == ')':
            opensofar -= 1
            if opensofar == 0:
                return idx


def rparse(eq):
    if len(eq) == 1:
        return int(eq[0])
    for idx, val in enumerate(eq):
        if val == '(':
            cidx = find_cbracket(eq)
            return rparse(eq[:idx] + [rparse(eq[idx+1:cidx])] + eq[cidx+1:])
    if eq[-2] == '+':
        return rparse([rparse(eq[:-2]) + int(eq[-1])])
    else:
        return rparse([rparse(eq[:-2]) * int(eq[-1])])


def bparse(eq):
    if len(eq) == 1:
        return int(eq[0])
    for idx, val in enumerate(eq):
        if val == '(':
            cidx = find_cbracket(eq)
            return bparse(eq[:idx] + [bparse(eq[idx+1:cidx])] + eq[cidx+1:])
    for idx, val in enumerate(eq):
        if val == '*':
            return bparse([bparse(eq[:idx]) * bparse(eq[idx+1:])])
    for idx, val in enumerate(eq):
        if val == '+':
            return bparse([bparse(eq[:idx]) + bparse(eq[idx+1:])])


def get_result(line_list, part):
    if part == 1:
        return sum((rparse([i for i in ''.join(eq.split())])
                   for eq in line_list))
    elif part == 2:
        return sum((bparse([i for i in ''.join(eq.split())])
                   for eq in line_list))


def test(day, targetvals):
    # Open test data, split by eq
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
        # Open input data, split by eq
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
