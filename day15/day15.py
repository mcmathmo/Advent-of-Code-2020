from time import perf_counter


def number_game(starting_nums, N):
    startnums = starting_nums.split(',')
    numdict = dict()
    idx = 1
    for num in startnums:
        numdict[int(num)] = idx
        idx += 1
    lastnum = int(startnums[-1])
    while idx < N + 1:
        if lastnum in numdict:
            nextnum = idx - 1 - numdict[lastnum]
            numdict[lastnum] = idx - 1
        else:
            nextnum = 0
            numdict[lastnum] = idx - 1
        lastnum = nextnum
        idx += 1
    return lastnum


def get_result(line_list, part):
    if part == 1:
        return number_game(line_list[0], 2020)
    elif part == 2:
        return number_game(line_list[0], 30000000)


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
    day = 15
    testvals = [436, 175594]
    main()

