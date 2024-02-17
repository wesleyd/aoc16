#!/usr/bin/env python3

from typing import List, Optional, Tuple

KEYPAD = """  1\n 234\n56789\n ABC\n  D""".splitlines()

def key_at(row, col):
    if row < 0 or len(KEYPAD) <= row:
        return ' '
    if col < 0 or len(KEYPAD[row]) <= col:
        return ' '
    return KEYPAD[row][col]

def find(n: str) -> Optional[Tuple[int, int]]:
    for row, r in enumerate(KEYPAD):
        for col, c in enumerate(r):
            if c == n:
                return (row, col)
assert find('4') == (1, 3)
assert find('9') == (2,4)
assert find('A') == (3, 1)

def move1(path: str, n: str = '5') -> str:
    row, col = find(n)
    for d in path:
        row2, col2 = row, col
        match d:
            case 'U':
                row2 -= 1
            case 'D':
                row2 += 1
            case 'L':
                col2 -= 1
            case 'R':
                col2 += 1
        if key_at(row2, col2) == ' ':
            continue
        row = row2
        col = col2
    return KEYPAD[row][col]
assert move1('ULL', '5') == '5'
assert move1('RRDDD', '5') == 'D'
assert move1('LURDL', 'D') == 'B'
assert move1('UUUUD', 'B') == '3'

example_input = """
ULL
RRDDD
LURDL
UUUUD
"""

def move(paths: List[str], n: str = '5'):
    code = []
    for path in paths:
        n = move1(path, n)
        code += n
    return ''.join(code)
assert move(example_input.strip().splitlines()) == '5DB3'

real_input = open('inputs/day02.input.txt').read()
print(move(real_input.strip().splitlines()))  # => 9A7DC
