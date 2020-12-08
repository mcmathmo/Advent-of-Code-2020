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


def correct_code_fast(line_list):
    maxidx = len(line_list)
    idx = 0
    oldidx = 0
    oldaccum = 0
    switched = False
    accum = 0
    while idx < maxidx:
        # something weird happening around idx 479, gets caught in loop
        if idx == 479:
            print('idx 479')
        if line_list[idx] == 'seen':
            idx = oldidx
            accum = oldaccum
            switched = False
        elif line_list[idx][:3] == 'acc':
            accum += int(line_list[idx].split()[-1])
            line_list[idx] = 'seen'
            idx += 1
        elif line_list[idx][:3] == 'jmp':
            jump = int(line_list[idx].split()[-1])
            line_list[idx] = 'seen'
            if switched:
                idx += jump
            else:
                switched = True
                oldidx = idx + jump
                if oldidx == 479:
                    print('479')
                oldaccum = accum
                idx += 1
        elif line_list[idx][:3] == 'nop':
            jump = int(line_list[idx].split()[-1])
            line_list[idx] = 'seen'
            if switched:
                idx += 1
            else:
                switched = True
                oldidx = idx + 1
                oldaccum = accum
                idx += jump
        else:
            print('weird')
            print(f'idx is {idx}')
            print(line_list[idx])

    return accum


def get_result(line_list, part):
    if part == 1:
        return process_code(line_list)[0]
    if part == 2:
        return correct_code_fast(line_list)


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
