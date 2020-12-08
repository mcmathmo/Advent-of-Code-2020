from time import perf_counter


def process_code(line_list):
    accum, i = 0, 0
    i_visited = set()
    # Stop loop if seen instruction before
    while i not in i_visited:
        # Iterate through unseen instructions
        if line_list[i][:3] == 'acc':
            i_visited.add(i)
            accum += int(line_list[i].split()[-1])
            i += 1
        elif line_list[i][:3] == 'jmp':
            i_visited.add(i)
            i += int(line_list[i].split()[-1])
        elif line_list[i][:3] == 'nop':
            i_visited.add(i)
            i += 1
    return accum, (i_visited, accum)


def correct_code(line_list):
    maxi = len(line_list)
    switch_idx = set()
    for idx in process_code(line_list)[1][0]:
        # Store changeable instructions in a set
        if line_list[idx][:3] != 'acc':
            switch_idx.add(idx)
    # Try changing jmp instructions first
    while switch_idx:
        change_idx = switch_idx.pop()
        # Switch instruction
        switch = ('jmp', 'nop')
        if line_list[change_idx][:3] == 'nop':
            switch = switch[::-1]
        line_list[change_idx] = line_list[change_idx].replace(*switch)
        i = 0
        accum = 0
        i_visited = set()
        while i not in i_visited:
            # Check if finished
            if i == maxi:
                return accum
            if line_list[i][:3] == 'acc':
                i_visited.add(i)
                accum += int(line_list[i].split()[-1])
                i += 1
            elif line_list[i][:3] == 'jmp':
                i_visited.add(i)
                i += int(line_list[i].split()[-1])
            elif line_list[i][:3] == 'nop':
                i_visited.add(i)
                i += 1
        # Revert changed instruction
        line_list[change_idx] = line_list[change_idx].replace(*switch[::-1])
    print('Never terminated')


def get_result(line_list, part):
    if part == 1:
        return process_code(line_list)[0]
    if part == 2:
        return correct_code(line_list)


def test(day, targetvals):
    # Open test data, split by line
    with open("day" + str(day) + "_test.txt") as input_file:
        read_data = input_file.read()
        line_list = read_data.split('\n')
    resultvals = [0 for _ in range(len(targetvals))]
    for i, _ in enumerate(targetvals):
        resultvals[i] = get_result(line_list, i+1)
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
            output = get_result(line_list, i+1)
            toc = perf_counter()
            print(f'Part {i+1}: {output}')
            print(f'This took {toc-tic:0.7f} seconds')



if __name__ == "__main__":
    day = 8
    testvals = [5, 8]
    main()
