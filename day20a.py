#!/usr/bin/env python3

import re

example_input = """
5-8
0-2
4-7
"""

def numbers(s):
    for n in re.findall(f'\d+', s):
        yield int(n)

def parse(inp):
    return [tuple(numbers(line)) for line in inp.strip().splitlines()]

def run(intervals):
    intervals.sort()
    lowest = 0
    for iv in intervals:
        if lowest < iv[0]:
            return lowest
        elif lowest <= iv[1]:
            lowest = iv[1]+1
    return lowest
assert (n := run(parse(example_input))) == 3, n

real_input = open('inputs/day20.input.txt').read()
print(run(parse(real_input))) # => 14975795
