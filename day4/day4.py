# -*- coding: utf-8 -*-

import re

required_fields = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
eye_colours = {'amb','blu','brn','gry','grn','hzl','oth'}

class Passport:
    def __init__(self, args):
        for attr in required_fields:
            setattr(self, attr, None)
        for entry in args:
            setattr(self, entry[:3], entry[4:])

    def hasfields(self):
        for attr in required_fields:
            if getattr(self, attr) is None:
                return False
        return True

    def byrcheck(self):
        if not re.match('^[0-9]{4}$',self.byr):
            return False
        elif not 1920 <= int(self.byr) <= 2002:
            return False
        return True

    def iyrcheck(self):
        if not re.match('^[0-9]{4}$',self.iyr):
            return False
        elif not 2010 <= int(self.iyr) <= 2020:
            return False
        return True

    def eyrcheck(self):
        if not re.match('^[0-9]{4}$',self.eyr):
            return False
        elif not 2020 <= int(self.eyr) <= 2030:
            return False
        return True

    def hgtcheck(self):
        if not re.match('^[0-9]*((cm)|(in))$',self.hgt):
            return False
        elif self.hgt[-2:] == 'cm' and not 150 <= int(self.hgt[:-2]) <= 193:
            return False
        elif self.hgt[-2:] == 'in' and not 59 <= int(self.hgt[:-2]) <= 76:
            return False
        return True

    def hclcheck(self):
        return re.match('^#[0-9a-f]{6}$',self.hcl)

    def eclcheck(self):
        return self.ecl in eye_colours

    def pidcheck(self):
        return re.match('^[0-9]{9}',self.pid)


def datavalidate(passp):
    if not passp.hasfields():
       return False
    checkdict = {'byr': Passport.byrcheck,
                 'iyr': Passport.iyrcheck,
                 'eyr': Passport.eyrcheck,
                 'hgt': Passport.hgtcheck,
                 'hcl': Passport.hclcheck,
                 'ecl': Passport.eclcheck,
                 'pid': Passport.pidcheck}
    return all((checkdict[field](passp) for field in required_fields))


def check_passports(line_list):
    return sum([Passport(line.split()).hasfields() for line in line_list])


def check_validate_passports(line_list):
    return sum([datavalidate(Passport(line.split())) for line in line_list])


def masterfunc(line_list, part):
    if part == 1:
        return check_passports(line_list)
    if part == 2:
        return check_validate_passports(line_list)


def test(day, targetvals):
    with open("day" + str(day) + "_test.txt") as input_file:
        read_data = input_file.read()
        line_list = read_data.split('\n\n')
    resultvals = [0 for _ in range(len(targetvals))]
    for i, _ in enumerate(targetvals):
        resultvals[i] = masterfunc(line_list, i+1)
        if resultvals[i] != testvals[i]:
            print(f'Test part {i+1} fails: expected '
                  f'{testvals[i]} but got {resultvals[i]}')
    return resultvals == testvals

if __name__ == "__main__":
    day = 4
    testvals = [2,2]
    if test(day, testvals):
        with open("day" + str(day) + "_input.txt") as input_file:
            read_data = input_file.read()
            line_list = read_data.split('\n\n')
        for i, _ in enumerate(testvals):
            output = masterfunc(line_list, i+1)
            print(f'Part {i+1}: {output}')
