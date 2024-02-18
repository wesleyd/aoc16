#!/usr/bin/env python3

import re

example_input = """
rect 3x2
rotate column x=1 by 1
rotate row y=0 by 4
rotate column x=1 by 1
"""

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.g = [['.'] * width for _ in range(height)]
    def print(self):
        for row in self.g:
            print(''.join(row))
    def nlit(self):
        return sum(sum(1 if ch == '#' else 0 for ch in r) for r in self.g)

def rect(g, w, h):
    for r in range(h):
        for c in range(w):
            g.g[r][c] = '#'

def rotate_column(g, c, n):
    if n < 0:
        n = height + n
    while n:
        old = [g.g[r][c] for r in range(g.height)]
        old = [old[-1]] + old[0:-1]
        for r, ch in enumerate(old):
            g.g[r][c] = ch
        n -= 1

def rotate_row(g, r, n):
    n = -n
    if n < 0:
        n = g.width + n
    g.g[r] = g.g[r][n:] + g.g[r][:n] 

g = Grid(7, 3)
rect(g, 3, 2)
#g.print()
rotate_column(g, 1, 1)
#g.print()
rotate_row(g, 0, 4)
#g.print()
rotate_column(g, 1, 1)
#g.print()
assert g.nlit() == 6

def run(inp, w, h):
    g = Grid(w, h)
    for line in inp.strip().splitlines():
        a, b = (int(x) for x in re.findall(r'\d+', line))
        if line.startswith('rect'):
            rect(g, a, b)
        elif line.startswith('rotate column'):
            rotate_column(g, a, b)
        elif line.startswith('rotate row'):
            rotate_row(g, a, b)
    return g.nlit()

real_input = open('inputs/day08.input.txt').read()
print(run(real_input, 50, 6))  # => 128
