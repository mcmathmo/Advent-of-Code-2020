from time import perf_counter


def loop(value, subject_number):
    return (value*subject_number) % 20201227


def find_loop_size(line_list):
    card_pub = int(line_list[0])
    door_pub = int(line_list[1])
    pub_keys = set((card_pub, door_pub))
    value = 1
    loops = 0
    loop_sizes = set()
    while pub_keys:
        if value in pub_keys:
            print(f"Matched {value} in {loops} loops")
            pub_keys.remove(value)
            loop_sizes.add(loops)
            maxloop = value
        value = loop(value, 7)
        loops += 1
    encrypt_key = 1
    for _ in range(min(loop_sizes)):
        encrypt_key = loop(encrypt_key, maxloop)
    return encrypt_key


def get_result(line_list, part):
    if part == 1:
        return find_loop_size(line_list)
    elif part == 2:
        return


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
    day = 25
    testvals = [14897079]
    main()

