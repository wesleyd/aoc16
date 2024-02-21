#!/usr/bin/env python3

import re
import itertools

from heapdict import heapdict
from copy import deepcopy

example_input = """
The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant.
"""

nths = {
    'first': 0,
    'second': 1,
    'third': 2,
    'fourth': 3,
}

class Facility:
    def __init__(self, inp):
        self.elevator = 0
        self.floors = [set(), set(), set(), set()]
        for line in inp.strip().splitlines():
            floor = None
            for nth, idx in nths.items():
                if nth in line:
                    floor = self.floors[idx]
                    break
            gens = re.findall('([a-z]+) generator', line)
            for gen in gens:
                floor.add(gen[0].upper() + 'G')
            chips = re.findall('([a-z]+)-compatible microchip', line)
            for chip in chips:
                floor.add(chip[0].upper() + 'M')
    def __hash__(self):
        ff = [tuple(sorted(f)) for f in self.floors]
        return hash((self.elevator, tuple(ff)))
    def __eq__(self, other):
        if self.elevator != other.elevator:
            return False
        for i in range(3):
            if self.floors[i] != other.floors[i]:
                return False
        return True
    def __str__(self):
        lines = []
        for i, floor in enumerate(self.floors):
            e = 'E' if self.elevator == i else ' '
            lines.append(f'F{i+1} {e} {floor}')
        lines.reverse()
        return '\n'.join(lines)
    def safe(self):
        for floor in self.floors:
            if not safe_combo(floor):
                return False
        return True

def safe_combo(items):
    microchips, generators = set(), set()
    for item in items:
        if item[1] == 'M':
            microchips.add(item[0])
        elif item[1] == 'G':
            generators.add(item[0])
        else:
            assert False, f'bad item {item} in {items}'
    for m in microchips:
        if m in generators:
            continue
        if generators:
            return False
    return True
assert safe_combo(['HM', 'LM'])
assert safe_combo(['HG', 'HM'])
assert safe_combo(['HG', 'HM', 'LG'])
assert safe_combo(['HG'])
assert safe_combo(['HG', 'HM', 'LG', 'LM'])
assert not safe_combo (['HG', 'HM', 'LM'])

def moved(facility, to, items):
    """Returns a new facility, with items moved to to, or None if not allowed."""
    facility = deepcopy(facility)
    items = set(items)
    if len(items) < 1 or len(items) > 2:
        return
    #if not safe_combo(items):
    #    return
    facility.floors[facility.elevator] -= items
    facility.floors[to] |= items
    facility.elevator = to
    #print("Safe?")
    #print(facility)
    if not facility.safe():
        #print("NOT SAFE")
        return
    #print("SAFE")
    #print()
    return facility

# print(Facility(example_input))

def moves(facility):
    e = facility.elevator
    for e2 in [e-1, e+1]:
        if e2 < 0 or e2 >= 4:
            continue
        for n in [1, 2]:
            for items in itertools.combinations(facility.floors[facility.elevator], n):
                #print(f'Move {n} items {items} to {e2}?')
                g = moved(facility, e2, items)
                if g:
                    #print('  Yes')
                    yield g
                else:
                    #print('  No')
                    pass

def win(facility):
    return not facility.floors[0] and not facility.floors[1] and not facility.floors[2]

# f = Facility('')
# f.elevator = 3
# f.floors[3] = set(['HG', 'HM', 'LG', 'LM'])
# print(win(f))

# f = Facility(example_input)
# print(f)
# for g in moves(f):
#     print(g)

# f = Facility

def play(inp):
    f = Facility(inp)
    future = heapdict()
    prev = {}
    future[f] = 0
    furthest = 0
    while future:
        f, dist = future.popitem()
        if dist > furthest:
            print(dist)
            furthest = dist
        #print(dist)
        #print(f)
        #print()
        if win(f):
            return dist
        for f2 in moves(f):
            if f2 in prev or f2 in future:
                continue
            future[f2] = dist + 1
            prev[f2] = f            
print(play(example_input))

# f = Facility(example_input)
# while True:
#     print('Currently:')
#     print(f)
#     print()
#     print('Moves:')
#     mm = list(moves(f))
#     for i, f2 in enumerate(mm):
#         print(f'#{i}')
#         print(f2)
#         print()
#     j = -1
#     while j < 0 or len(mm) <= j:
#         j = int(input(f'0-{len(mm)-1}? '))
#     f = mm[j]
    
# f = Facility('')
# f.elevator = 3
# f.floors[3] = set(['HG', 'LG', 'LM'])
# f.floors[2] = set(['HM'])
# print(f.__hash__())
# dd = set()
# dd.add(f)
# g = Facility('')
# g.elevator = 3
# g.floors[3] = set(['HG', 'LG', 'LM'])
# g.floors[2] = set(['HM'])
# print(g.__hash__())
# print(g in dd)

real_input = open('inputs/day11.input.txt').read()
print(play(real_input)) # => 37
