from time import perf_counter


def playdict(nums, iters, maxnum):
    nums = [int(x) for x in nums]
    current_cup = nums[0]
    numdict = {i: i+1 for i in range(max(nums)+1, maxnum+1)}
    for i in range(len(nums)-1):
        numdict[nums[i]] = nums[i+1]
    if maxnum > max(nums):
        numdict[nums[-1]] = max(nums) + 1
        numdict[maxnum] = nums[0]
    else:
        numdict[nums[-1]] = nums[0]
    # numdict key is a number x, and value is the number after x in the circle
    for k in range(iters):
        pick1 = numdict[current_cup]
        pick2 = numdict[pick1]
        pick3 = numdict[pick2]
        destination_cup = ((current_cup - 2) % maxnum) + 1
        while destination_cup in (pick1, pick2, pick3):
            destination_cup = ((destination_cup - 2) % maxnum) + 1

        numdict[current_cup] = numdict[pick3]
        current_cup = numdict[pick3]
        numdict[pick3] = numdict[destination_cup]
        numdict[destination_cup] = pick1
    return numdict


def get_result(line_list, part):
    if part == 1:
        nums = playdict(line_list[0], 100, 9)
        ans = []
        curval = 1
        for i in range(len(nums)-1):
            curval = nums[curval]
            ans.append(str(curval))
        return ''.join(ans)
    elif part == 2:
        numdict = playdict(line_list[0], 10000000, 1000000)
        return numdict[1] * numdict[numdict[1]]


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
    day = 23
    testvals = ['67384529', 149245887792]
    main()
