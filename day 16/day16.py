from time import perf_counter
from math import prod


class Ticket_validator:
    def __init__(self, rules):
        self.ruleset = []
        for line in rules:
            rule = set()
            line = line.split()
            rule_one = line[-1].split('-')
            rule_two = line[-3].split('-')
            for i in range(int(rule_one[0]), int(rule_one[1])+1):
                rule.add(i)
            for i in range(int(rule_two[0]), int(rule_two[1])+1):
                rule.add(i)
            self.ruleset.append(rule)
        self.megaset = set().union(*self.ruleset)

    def quickcheck(self, val):
        return val in self.megaset

    def check(self, val, rule_idx):
        return val in self.ruleset[rule_idx]


def nearby_invalids(lines, validator):
    near_vals = [int(x) for x in ','.join(lines[2].split('\n')[1:]).split(',')]
    return sum((val for val in near_vals if not validator.quickcheck(val)))


def check_ticket(ticket, tvalidator):
    return all((tvalidator.quickcheck(val)) for val in ticket)


def discard_invalids(lines, validator):
    near_tickets = [[int(x) for x in ticket.split(',')]
                    for ticket in lines[2].split('\n')[1:]]
    return [tick for tick in near_tickets if check_ticket(tick, validator)]


def identify_field(line_list, validator):
    # rulemap is a one-to-many mapping of column to rules satisfied
    rulesat = dict()
    valid_tickets = discard_invalids(line_list, validator)
    numrules = len(valid_tickets[0])
    for col_idx in range(numrules):
        rulesat[col_idx] = set()
        for rule_idx in range(numrules):
            if all((validator.check(ticket[col_idx], rule_idx)
                    for ticket in valid_tickets)):
                rulesat[col_idx].add(rule_idx)
    # Deduce the unique col-->rule map
    rulemap = dict()
    for attempt in range(numrules):
        for col in rulesat:
            # Remove rules that are already in the unique map
            for rule in rulemap.values():
                if rule in rulesat[col]:
                    rulesat[col].remove(rule)
            # If there is only one possibility then it is the solution
            if len(rulesat[col]) == 1:
                rulemap[col] = min(rulesat[col])
    return rulemap


def sum_departure(line_list, validator):
    myticket = [int(x) for x in line_list[1].split('\n')[1].split(',')]
    rulemap = identify_field(line_list, validator)
    return prod((val for idx, val in enumerate(myticket) if rulemap[idx] < 6))


def get_result(line_list, part):
    rule_list = line_list[0].split('\n')
    validator = Ticket_validator(rule_list)
    if part == 1:
        return nearby_invalids(line_list, validator)
    elif part == 2:
        return sum_departure(line_list, validator)


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
    day = 16
    testvals = [0, 1716]
    main()
