from time import perf_counter


def init_bag_map(line_list):
    mapdict = dict()
    for line in line_list:
        splitline = line.split()
        key = ' '.join(splitline[:2])
        mapdict[key] = set()
        for idx, val in enumerate(splitline[3:]):
            if val[:3] == 'bag':
                newbag = ' '.join(splitline[idx+1:idx+3])
                mapdict[key].add(newbag)
    return mapdict


def invert_map(bag_map):
    revmap = dict()
    for oldkey, set_of_keys in bag_map.items():
        for newkey in set_of_keys:
            revmap.setdefault(newkey, set()).add(oldkey)
    del revmap['no other']
    return revmap


def find_outer_bags(revmap, startbag):
    outerbags = {bag for bag in revmap[startbag]}
    bags_to_check = {bag for bag in revmap[startbag]}
    while len(bags_to_check) != 0:
        nextbag = bags_to_check.pop()
        if nextbag not in revmap:
            outerbags.add(nextbag)
            continue
        for bag in revmap[nextbag]:
            if bag not in outerbags:
                outerbags.add(bag)
                bags_to_check.add(bag)
    return outerbags


def init_bag_multmap(line_list):
    mapdict = dict()
    for line in line_list:
        splitline = line.split()
        key = ' '.join(splitline[:2])
        mapdict[key] = set()
        for idx, val in enumerate(splitline[3:]):
            if val[:3] == 'bag':
                newbag = (splitline[idx],
                          ' '.join(splitline[idx+1:idx+3]))
                mapdict[key].add(newbag)
    return mapdict


def bags_contained(curbag):
    if curbag in cache:
        return cache[curbag]
    if ('contain', 'no other') in bag_map[curbag[1]]:
        cache[curbag[1]] = 0
        return 0
    result = sum((int(bag[0])*(bags_contained(bag)+1)
                  for bag in bag_map[curbag[1]]))
    cache[curbag] = result
    return result


def get_result(line_list, part):
    if part == 1:
        return len(find_outer_bags(invert_map(init_bag_map(line_list)),
                                   'shiny gold'))
    if part == 2:
        global bag_map
        global cache
        bag_map = init_bag_multmap(line_list)
        cache = dict()
        return bags_contained((1, 'shiny gold'))


def main():
    tic = perf_counter()
    with open("day7_large_input.txt") as input_file:
        read_data = input_file.read()
        line_list = read_data.split('\n')
    for i, _ in enumerate(testvals):
        output = get_result(line_list, i+1)
        print(f'Part {i+1}: {output}')
    toc = perf_counter()
    print(f'This took {toc-tic:0.7f} seconds')


if __name__ == "__main__":
    day = 7
    testvals = [4, 32]
    main()
