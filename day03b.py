#!/usr/bin/env python3

import re

def possible(a,b,c):
    return a+b>c and a+c>b and b+c>a
assert not possible(5,10,25)

def parse(inp):
    tt = []
    for line in inp.strip().splitlines():
        tt.append([int(x) for x in re.findall(r'\d+', line)])
    i = 0
    while i < len(tt):
        tt[i+1][0], tt[i][1] = tt[i][1], tt[i+1][0]
        tt[i+2][0], tt[i][2] = tt[i][2], tt[i+2][0]
        tt[i+2][1], tt[i+1][2] = tt[i+1][2], tt[i+2][1]
        i += 3
    return tt
    
def count_possibles(tuples):
    nposs = 0
    for t in tuples:
        if possible(*t):
            nposs += 1
    return nposs

real_input = open('inputs/day03.input.txt').read()
real_tuples = parse(real_input)

print(count_possibles(real_tuples)) # 1826
