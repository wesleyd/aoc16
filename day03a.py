#!/usr/bin/env python3

import re

def possible(a,b,c):
    return a+b>c and a+c>b and b+c>a
assert not possible(5,10,25)

def parse(inp):
    tuples = []
    for line in inp.strip().splitlines():
        tuples.append(tuple([int(x) for x in re.findall(r'\d+', line)]))
    return tuples
assert parse("5 10 25") == [(5,10,25)]

def count_possibles(tuples):
    nposs = 0
    for t in tuples:
        if possible(*t):
            nposs += 1
    return nposs

real_input = open('inputs/day03.input.txt').read()
real_tuples = parse(real_input)

print(count_possibles(real_tuples)) # 982
