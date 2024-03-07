#!/usr/bin/env python3
# It turns out that there is only one "hole".
# Part 1 shows that of all the possible moves, they all point to one node!
# That is, all the useds (but one) are bigger than all the avails (but one!)
# And some nodes can never move - they are like walls in a maze.
#
# So, if we regard this as moving THE ONE HOLE around to get Gold to Origin...
#   Find shortest path from G to O. Move G along it by...
#   While G != (0,0):
#     Find shortest path from _ to next along G's path. Add that.
#     (Hole can Only move along '.'s)
#     Swap G and hole. Add 1.
#
# This might not be the shortest path _in all cases_. This adds up shortest
# paths for multiple steps, and there *might* exist a case where the shortest
# path (over '.'s) from G to O doesn't lead to the total number of data moves.
# I don't think we need to worry about that though, if it even _is_ a worry.

import math
import re

from collections import namedtuple
from heapdict import heapdict

example_input = """
Filesystem            Size  Used  Avail  Use%
/dev/grid/node-x0-y0   10T    8T     2T   80%
/dev/grid/node-x0-y1   11T    6T     5T   54%
/dev/grid/node-x0-y2   32T   28T     4T   87%
/dev/grid/node-x1-y0    9T    7T     2T   77%
/dev/grid/node-x1-y1    8T    0T     8T    0%
/dev/grid/node-x1-y2   11T    7T     4T   63%
/dev/grid/node-x2-y0   10T    6T     4T   60%
/dev/grid/node-x2-y1    9T    8T     1T   88%
/dev/grid/node-x2-y2    9T    6T     3T   66%
"""

Point = namedtuple('Point', ['x', 'y'])

def up(p: Point) -> Point:
    return Point(p.x, p.y-1)
def down(p: Point) -> Point:
    return Point(p.x, p.y+1)
def left(p: Point) -> Point:
    return Point(p.x-1, p.y)
def right(p: Point) -> Point:
    return Point(p.x+1, p.y)

Node = namedtuple('Node', ['used', 'avail', 'size'])

def extract_numbers(s):
    for n in re.findall(r'\d+', s):
        yield int(n)

class Grid(object):
    def __init__(self, inp):
        # First parse to dict...
        nodes = {}
        xmax = -math.inf
        ymax = -math.inf
        for line in inp.strip().splitlines():
            if not line.startswith('/dev'):
                continue
            x, y, size, used, avail, _ = extract_numbers(line)
            assert used+avail == size, line
            nodes[Point(x,y)] = Node(used, avail, size)
            if x > xmax:
                xmax = x
            if y > ymax:
                ymax = y
        width, height = xmax+1, ymax+1
        # Convert to a grid, and make sure there's only one hole...
        can_move = set()
        hole = None
        for p, n in nodes.items():
            for q, m in nodes.items():
                if p == q:
                    continue
                if n.used == 0:
                    continue
                if n.used <= m.avail:
                    assert not hole or q == hole, f'>1 hole {hole} v {q}={m=}'
                    hole = q
                    can_move.add(p)
        grid = [['#' for x in range(width)] for y in range(height)]
        grid[hole.y][hole.x] = '_'
        for p in can_move:
            grid[p.y][p.x] = '.'
        grid[0][0] = 'O'
        grid[0][xmax]= 'G'
        self.g = grid
        self.width = width
        self.height = height
        self.hole = hole
        self.gold = Point(xmax, 0)
        self.nodes = nodes
    def at(self, p):
        if p.y < 0 or len(self.g) <= p.y:
            return '#'
        if p.x < 0 or len(self.g[p.y]) <= p.x:
            return '#'
        return self.g[p.y][p.x]
    def __str__(self):
        return '\n'.join(''.join(c for c in line) for line in self.g)

def retrace(q, prev):
    path = []
    while q:
        path.append(q)
        q = prev.get(q, None)
    path.reverse()
    return path

def shortest_path(grid, a, z):
    futures = heapdict()
    gold = Point(len(grid.g[0])-1, 0)
    futures[a] = 0
    dist = {a: 0}
    prev = {}
    while futures:
        p, cost  = futures.popitem()
        alt = cost + 1
        for q in [up(p), down(p), left(p), right(p)]:
            if q == z:
                prev[q] = p
                return retrace(q, prev)
            if grid.at(q) in 'G#':
                continue
            if alt < dist.get(q, math.inf):
                dist[q] = alt
                futures[q] = alt
                prev[q] = p

def shortest_path_G_to_O(grid):
    """Returns the shortest path from G to O."""
    return shortest_path(grid, grid.gold, Point(0,0))

def move_hole_to(grid, p):
    """Moves hole to p as cheaply as possible; returns num steps."""
    path = shortest_path(grid, grid.hole, p)
    h = grid.hole
    grid.g[h.y][h.x], grid.g[p.y][p.x] = grid.g[p.y][p.x], grid.g[h.y][h.x]
    if grid.gold == p:
        grid.gold = grid.hole
    grid.hole = p
    return len(path)

def move_gold_to_origin(grid):
    """Moves gold to origin as cheaply as possible; returns number of steps."""
    gold_path = shortest_path(grid, grid.gold, Point(0,0))
    gold = gold_path.pop(0)
    steps = 0
    while gold_path:
        next_gold = gold_path.pop(0)
        # Move the hole to where it needs to be
        steps += move_hole_to(grid, next_gold) - 1
        # Swap gold and hole
        steps += move_hole_to(grid, gold) - 1
        gold = next_gold
    return steps

example_grid = Grid(example_input)
assert move_gold_to_origin(example_grid) == 7

real_input = open('inputs/day22.input.txt').read()
real_grid = Grid(real_input)
#print(real_grid)
#print(shortest_path_G_to_O(real_grid))
print(move_gold_to_origin(real_grid))  # => 188
