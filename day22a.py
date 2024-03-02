#!/usr/bin/env python3

import re

from collections import namedtuple

Node = namedtuple('Node', ['x', 'y', 'size', 'used', 'avail'])

def numbers(s):
    for n in re.findall(r'\d+', s):
        yield int(n)

def parse(inp):
    nodes = []
    for line in inp.strip().splitlines():
        if not line.startswith('/dev'):
            continue
        x, y, size, used, avail, _ = numbers(line)
        nodes.append(Node(x, y, size, used, avail))
    return nodes

def count_viable_pairs(nodes):
    n = 0
    for a in nodes:
        for b in nodes:
            if a == b:
                continue
            if a.used == 0:
                continue
            if a.used <= b.avail:
                n += 1
    return n

real_input = open('inputs/day22.input.txt').read()
real_nodes = parse(real_input)

print(count_viable_pairs(real_nodes))  # => 937
