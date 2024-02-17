#!/usr/bin/env python3

from typing import List, Optional, Tuple

KEYPAD = """
123
456
789
""".strip().splitlines()

def find(n: int|str) -> Optional[Tuple[int, int]]:
    for row, r in enumerate(KEYPAD):
        for col, c in enumerate(r):
            if int(c) == int(n):
                return (row, col)
assert find(4) == (1, 0)
assert find(9) == (2, 2)

def clamp(n, b):
    if n < 0:
        return 0
    if n > b:
        return b
    return n

def move1(path: str, n: int|str = 5) -> str:
    row, col = find(n)
    for d in path:
        match d:
            case 'U':
                row -= 1
            case 'D':
                row += 1
            case 'L':
                col -= 1
            case 'R':
                col += 1
        row = clamp(row, len(KEYPAD)-1)
        col = clamp(col, len(KEYPAD[0])-1)
    return KEYPAD[row][col]
assert move1('ULL', 5) == '1'
assert move1('RRDDD', 1) == '9'
assert move1('LURDL', 9) == '8'
assert move1('UUUUD', 8) == '5'

def move(paths: List[str], n: int|str = 5):
    code = []
    for path in paths:
        n = move1(path, n)
        code += n
    return ''.join(code)

example_input = """
ULL
RRDDD
LURDL
UUUUD
"""
assert move(example_input.strip().splitlines()) == '1985'

real_input = open('inputs/day02.input.txt').read()
print(move(real_input.strip().splitlines()))  # => 97289
