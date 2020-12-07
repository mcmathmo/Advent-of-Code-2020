from collections import Counter


def count_letters(group):
    letter_count = Counter([q for q in group.replace('\n', '')])
    return len(letter_count)


def count_all_yes(group):
    people = group.count('\n') + 1
    letter_count = Counter([q for q in group.replace('\n', '')])
    return sum([q[1] == people for q in letter_count.items()])


def get_result(line_list, part):
    if part == 1:
        return sum((count_letters(group) for group in line_list))
    if part == 2:
        return sum((count_all_yes(group) for group in line_list))


def test(day, targetvals):
    with open("day" + str(day) + "_test.txt") as input_file:
        read_data = input_file.read()
        line_list = read_data.split('\n\n')
    resultvals = [0 for _ in range(len(targetvals))]
    for i, _ in enumerate(targetvals):
        resultvals[i] = get_result(line_list, i+1)
        if resultvals[i] != testvals[i]:
            print(f'Test part {i+1} fails: expected '
                  f'{testvals[i]} but got {resultvals[i]}')
    return resultvals == testvals


def main():
    if test(day, testvals):
        with open("day" + str(day) + "_input.txt") as input_file:
            read_data = input_file.read()
            line_list = read_data.split('\n\n')
        for i, _ in enumerate(testvals):
            output = get_result(line_list, i+1)
            print(f'Part {i+1}: {output}')


if __name__ == "__main__":
    day = 6
    testvals = [11, 6]
    main()
