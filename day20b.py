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

def run(intervals, low=0, high=4294967295):
    intervals.sort()
    for i,p in enumerate(intervals):
        assert p[0]<=p[1], f'{i=}, {p=}'
        assert low <= p[0], f'{low=}<={p=}'
        assert p[1] <= high, f'{p=}<={high=}'
    a = intervals[0]
    ips = a[0] - low
    for b in intervals[1:]:
        if b[1] < a[1]:
            continue
        if a[1] < b[0]:
            ips += b[0] - a[1] - 1
        a = b
    ips += high - a[1]
    return ips
assert run(parse(example_input), 0, 9) == 2

real_input = open('inputs/day20.input.txt').read()
print(run(parse(real_input))) # => 101
