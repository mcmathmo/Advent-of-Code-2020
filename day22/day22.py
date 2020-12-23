from time import perf_counter
from collections import deque


def combat(p1, p2):
    p1 = deque(p1)
    p2 = deque(p2)
    while p1 and p2:
        p1_card = p1.popleft()
        p2_card = p2.popleft()
        if p1_card > p2_card:
            p1.extend((p1_card, p2_card))
        else:
            p2.extend((p2_card, p1_card))
    return p1 + p2


def rec_combat(p1, p2):
    memo = set()
    while p1 and p2:
        # returns True if p1 wins, else False
        if (tuple(p1), tuple(p2)) in memo:
            # state seen before, p1 wins
            return True, p1 + p2
        else:
            memo.add((tuple(p1), tuple(p2)))

        p1_card = p1.pop(0)
        p2_card = p2.pop(0)
        if len(p1) >= p1_card and len(p2) >= p2_card:
            if rec_combat(p1[:p1_card], p2[:p2_card])[0]:
                p1.extend((p1_card, p2_card))
            else:
                p2.extend((p2_card, p1_card))
        else:
            if p1_card > p2_card:
                p1.extend((p1_card, p2_card))
            else:
                p2.extend((p2_card, p1_card))
    return bool(p1), p1 + p2


def get_result(line_list, part):
    p1 = [int(x) for x in line_list[0].split('\n')[1:]]
    p2 = [int(x) for x in line_list[1].split('\n')[1:]]
    if part == 1:
        return sum((idx+1)*val
                   for idx, val in enumerate(reversed(combat(p1, p2))))
    elif part == 2:
        return sum((idx+1)*val
                   for idx, val in enumerate(reversed(rec_combat(p1, p2)[1])))


def test(day, targetvals):
    # Open test data, split by line
    with open("day" + str(day) + "_test.txt") as input_file:
        read_data = input_file.read()
        line_list = read_data.split('\n\n')
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
            line_list = read_data.split('\n\n')
        for i, _ in enumerate(testvals):
            tic = perf_counter()
            output = get_result(line_list, i + 1)
            toc = perf_counter()
            print(f'Part {i+1}: {output}')
            print(f'This took {toc-tic:0.7f} seconds')


if __name__ == "__main__":
    day = 22
    testvals = [306, 291]
    main()
