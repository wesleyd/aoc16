#!/usr/bin/env python

import re

from collections import namedtuple

example_input = """
Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1.
"""

def extract_numbers(s):
    for n in re.findall(r'\d+', s):
        yield int(n)

Disc = namedtuple('Disc', ['start', 'mod'])

def parse(inp):
    discs = []
    for i, line in enumerate(inp.strip().splitlines()):
        nn = tuple(extract_numbers(line))
        discs.append(Disc(start=nn[3]+i, mod=nn[1]))
    return discs

def zeros(disc):
    n = disc.mod - disc.start
    while True:
        yield n
        n += disc.mod

def run(discs):
    zz = []
    for d in discs:
        zz.append(zeros(d))
    nn = [next(z) for z in zz]
    while True:
        #print(nn)
        m = max(nn)
        if all(n == m for n in nn):
            return m - 1
        for i, n in enumerate(nn):
            if n < m:
                nn[i] = next(zz[i])
run(parse(example_input))

real_input = open('inputs/day15.input.txt').read()
print(run(parse(real_input))) # => 122318

