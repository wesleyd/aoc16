#!/usr/bin/env python3

from heapdict import heapdict

class Office(object):
    def __init__(self, favorite_number):
        self.favorite_number = int(favorite_number)
        self.grid = {}
    def at(self, p):
        """Returns what is at p=(x,y)."""
        x, y = p
        if x < 0 or y < 0:
            return '#'
        s = self.grid.get(p, None) 
        if s is None:
            n = x*x + 3*x + 2*x*y + y + y*y + self.favorite_number
            if n.bit_count() % 2 == 0:
                s = '.'
            else:
                s = '#'
            self.grid[p] = s
        return s
    def moves(self, p):
        x, y = p
        for q in [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]:
            if self.at(q) == '.':
                yield q
    def draw(self, width=10, height=10):
        for y in range(height):
            for x in range(width):
                print(self.at((x,y)), end='')
            print()

def walk(office, max_steps=50, p=(1,1)):
    future = heapdict()
    future[p] = 0
    past = set()
    n = 0
    while future:
        p, dist = future.popitem()
        if dist > max_steps:
            return n
        if p in past:
            continue
        past.add(p)
        n += 1
        for q in office.moves(p):
            future[q] = dist+1

example_office = Office(10)
assert walk(example_office, 0) == 1
assert walk(example_office, 1) == 3
assert walk(example_office, 2) == 5

real_input = open('inputs/day13.input.txt').read()
real_office = Office(real_input)
print(walk(real_office))  # => 141
