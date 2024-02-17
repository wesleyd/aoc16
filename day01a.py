#!/usr/bin/env python3

import re

from collections import namedtuple

Instruction = namedtuple('Instruction', ['LR', 'N'])
def parse(inp):
    return [Instruction(LR=lr,N=int(n)) for lr, n in re.findall(r'([LR])(\d+)', inp)]

POINTS = "NESW"
At = namedtuple('At', ['point', 'x', 'y'])

def dist(at):
    return abs(at.x) + abs(at.y)

def turn(point, lr):
    n = POINTS.find(point)
    if lr == 'L':
        n -= 1
    elif lr == 'R':
        n += 1
    else:
        assert False, (point, lr, n)
    return POINTS[n%len(POINTS)]
assert turn('N', 'L') == 'W'
assert turn('E', 'R') == 'S'
assert turn('S', 'L') == 'E'
assert turn('W', 'R') == 'N'

def walk1(instr, at):
    point = turn(at.point, instr.LR)
    n = instr.N
    match point:
        case 'N':
            return At(point, at.x, at.y+n)
        case 'E':
            return At(point, at.x+n, at.y)
        case 'S':
            return At(point, at.x, at.y-n)
        case 'W':
            return At(point, at.x-n, at.y)
    assert False, (at, instr)

def walk(instructions, at=At('N', 0, 0)):
    visited = set()
    for instr in instructions:
        at = walk1(instr, at)
    return at

real_input = open('inputs/day01.input.txt').read()
real_instructions = parse(real_input)
print(dist(walk(parse(real_input)))) # => 278
