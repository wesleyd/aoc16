#!/usr/bin/env python3

import math

from collections import namedtuple
from heapdict import heapdict

example_input = """
###########
#0.1.....2#
#.#######.#
#4.......3#
###########
"""

Point = namedtuple('Point', ['row', 'col'])

def up(p):
    return Point(p.row-1,p.col)
def down(p):
    return Point(p.row+1,p.col)
def left(p):
    return Point(p.row,p.col-1)
def right(p):
    return Point(p.row,p.col+1)

NUMBERS = '0123456789'

def walk_from(maze, start='0'):
    futures = heapdict()
    p = maze.points[start]
    futures[p] = 0
    past = set()
    reachable = {}
    while futures:
        p, d = futures.popitem()
        past.add(p)
        for q in [up(p), down(p), left(p), right(p)]:
            if q in past or maze.at(q) == '#':
                continue
            ch = maze.at(q)
            if ch == '.':
                futures[q] = d+1
                continue
            assert ch in NUMBERS, (ch, q)
            assert ch != start, (ch, q)
            if ch not in reachable:
                reachable[ch] = d+1
            assert d+1 >= reachable[ch], (d+1, reachable[ch])
    return reachable

class Maze(object):
    def __init__(self, inp):
        self.cc = [list(line) for line in inp.strip().splitlines()]
        self.points = {}
        for row, line in enumerate(self.cc):
            for col, ch in enumerate(line):
                if ch in NUMBERS:
                    p = Point(row, col)
                    assert ch not in self.points, (ch, p)
                    self.points[ch] = p
        self.graph = {}
        for ch in self.points:
            self.graph[ch] = walk_from(self, ch)
    def at(self, p):
        if (p.row < 0 or len(self.cc) <= p.row):
            return '#'
        line = self.cc[p.row]
        if (p.col < 0 or len(line) <= p.col):
            return '#'
        return line[p.col]
    def cost(self, path):
        if not path:
            return 0
        n = 0
        for i in range(1, len(path)):
            n += self.graph[path[i-1]][path[i]]
        return n
    
maze = Maze(example_input)
assert Maze(example_input).graph == {
    '0': {'1': 2, '4': 2},
    '1': {'0': 2, '2': 6},
    '2': {'1': 6, '3': 2},
    '3': {'2': 2, '4': 8},
    '4': {'3': 8, '0': 2},
}

def pokemon_dfs(maze):
    cheapest = math.inf
    best = None
    goal = set(maze.graph)
    def helper(path):
        nonlocal cheapest, best
        cost = maze.cost(path)
        if cost > cheapest:
            return
        prev = set(path)
        dunroamin= False
        if prev == goal:
            dunroamin = True
        if dunroamin and path[-1] == '0':
            if cost < cheapest:
                cheapest = cost
                best = path
                print(f'Cheapest so far {cheapest}, {best}')
            return
        c = path[-1]
        nexts = set(maze.graph[c])
        if dunroamin:
            prev.remove('0')
        unvisited = nexts - prev
        visited = nexts & prev
        for d in unvisited:
            helper(path + (d,))
        for d in visited:
            helper(path + (d,))
    helper(('0',))
    return cheapest

real_input = open('inputs/day24.input.txt').read()
real_maze = Maze(real_input)
print(pokemon_dfs(real_maze))  # => 748
