from time import perf_counter


def create_sumset(nums):
    sumset = set()
    n = len(nums)
    for idx in range(n):
        for jdx in range(idx+1, n):
            sumset.add(nums[idx] + nums[jdx])
    return sumset


def get_invalid(nums):
    k = 25
    for i in range(k, len(nums)):
        sumset = create_sumset(nums[i-k:i])
        if nums[i] not in sumset:
            return nums[i]


def find_contig(nums, target):
    for lstlen in range(2, len(nums)):
        for i in range(len(nums)-lstlen):
            if sum(nums[i:i+lstlen]) == target:
                return min(nums[i:i+lstlen]) + max(nums[i:i+lstlen])


def get_result(line_list, part):
    nums = [int(line) for line in line_list]
    if part == 1:
        return get_invalid(nums)
    if part == 2:
        return find_contig(nums, get_invalid(nums))


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
    day = 9
    testvals = [None, None]
    main()
