from time import perf_counter
import re


class Rulechecker:
    def __init__(self, rule_list, part):
        self.rules = dict()
        for rule in rule_list:
            key, val = rule.split(': ')
            key = int(key)
            val = val.replace('"', '')
            if val in ['a', 'b']:
                self.rules[key] = val
            else:
                self.rules[key] = [[int(x) for x in part.split(' ')]
                                   for part in val.split(' | ')]
        if part == 2:
            self.rules[8] = [[42], [42, 8]]
            self.rules[11] = [[42, 31], [42, 11, 31]]

    def gen_regex(self, rulenum, depth):
        if depth > 14:
            return 'z'
        rule = self.rules[rulenum]
        if rule in ['a', 'b']:
            return rule
        regx_list = []
        for rulepart in rule:
            constr_regx = []
            for num in rulepart:
                constr_regx += [self.gen_regex(num, depth + 1)]
            regx_list.append(''.join(constr_regx))
        return ''.join(['(', '|'.join(regx_list), ')'])


def get_result(line_list, part):
    rules, msgs = line_list
    rule_list = rules.split('\n')
    msg_list = msgs.split('\n')
    checker = Rulechecker(rule_list, part)
    regx = re.compile(''.join(['^', checker.gen_regex(0, 0), '$']))
    return sum((bool(regx.match(msg)) for msg in msg_list))


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
    day = 19
    testvals = [3, 12]
    main()
