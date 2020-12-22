from time import perf_counter
from collections import defaultdict, Counter


def get_result(line_list, part):
    poss_ing = defaultdict(set)
    # key allergen : val ings that are possible for this allergen
    all_ings = Counter()
    for line in line_list:
        ings, allergens = line.split(' (contains ')
        ings = ings.split()
        allergens = allergens[:-1].split(', ')
        ing_set = set(ings)
        all_ings.update(ings)
        for allergen in allergens:
            if poss_ing[allergen]:
                poss_ing[allergen] = poss_ing[allergen].intersection(ing_set)
            else:
                poss_ing[allergen] = ing_set

    not_allergens = set(all_ings) - set().union(*poss_ing.values())
    if part == 1:
        return sum((all_ings[ing] for ing in not_allergens))

    dangerous_ing = dict()
    # key allergen : val ingredient
    for attempt in range(len(poss_ing)):
        for allergen in poss_ing:
            for ingredient in dangerous_ing.values():
                # remove ingredients we already know are another allergen
                if ingredient in poss_ing[allergen]:
                    poss_ing[allergen].remove(ingredient)
                # if there is one ingredient left then it must be the allergen
            if len(poss_ing[allergen]) == 1:
                dangerous_ing[allergen] = min(poss_ing[allergen])
    return ','.join((i[1] for i in sorted(dangerous_ing.items())))


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
    day = 21
    testvals = [5, 'mxmxvkd,sqjhc,fvjkl']
    main()
