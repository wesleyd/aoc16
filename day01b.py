#!/usr/bin/env python3

import re

from collections import namedtuple

Instruction = namedtuple('Instruction', ['LR', 'N'])
def parse(inp):
    return [Instruction(LR=lr,N=int(n)) for lr, n in re.findall(r'([LR])(\d+)', inp)]

COMPASS = "NESW"

Point = namedtuple('Point', ['x', 'y'])

def dist(p):
    return abs(p.x) + abs(p.y)

def turn(c, lr):
    n = COMPASS.find(c)
    if lr == 'L':
        n -= 1
    elif lr == 'R':
        n += 1
    else:
        assert False, (c, lr, n)
    return COMPASS[n%len(COMPASS)]
assert turn('N', 'L') == 'W'
assert turn('E', 'R') == 'S'
assert turn('S', 'L') == 'E'
assert turn('W', 'R') == 'N'

def walk1(instr, c, p):
    c = turn(c, instr.LR)
    for _ in range(instr.N):
        match c:
            case 'N':
                p = Point(p.x, p.y+1)
            case 'E':
                p = Point(p.x+1, p.y)
            case 'S':
                p = Point(p.x, p.y-1)
            case 'W':
                p = Point(p.x-1, p.y)
        yield c, p

def walk(instructions, c='N', p=Point(0, 0)):
    visited = set([p])
    for instr in instructions:
        for c, p in walk1(instr, c, p):
            if p in visited:
                return p
            visited.add(p)

assert dist(walk(parse('R8, R4, R4, R8'))) == 4

real_input = open('inputs/day01.input.txt').read()
real_instructions = parse(real_input)
print(dist(walk(parse(real_input))))  # => 161
