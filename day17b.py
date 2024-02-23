#!/usr/bin/env python3

import hashlib

def moves(s):
    """Yields all the legal moves from s."""
    for c, d in zip(hashlib.md5(s.encode()).hexdigest()[:4], 'UDLR'):
        if c in 'bcdef':
            yield d
assert (l := ''.join(list(moves('hijkl')))) == 'UDL', l
assert (l := ''.join(list(moves('hijklD')))) == 'ULR', l
assert (l := ''.join(list(moves('hijklDR')))) == '', l
assert (l := ''.join(list(moves('hijklDU')))) == 'R', l
assert (l := ''.join(list(moves('hijklDUR')))) == '', l

def pos(s):
    """Returns true if all positions s traverses are valid."""
    row, col = 0, 0
    for c in s:
        match c:
            case 'U':
                row -= 1
            case 'D':
                row += 1
            case 'L':
                col -= 1
            case 'R':
                col += 1
        if row < 0 or 4 <= row:
            return None
        if col < 0 or 4 <= col:
            return None
    return (row, col)

def walk(seed):
    """Returns the length of the longest path from s."""
    seen = set()
    futures = [seed]
    prev = set()
    longest = None
    while futures:
        p = futures.pop()
        if p in prev:
            continue
        prev.add(p)
        if not (rc := pos(p)):
            continue
        if rc == (3,3):
            if not longest or len(p) > len(longest):
                longest = p
            continue
        for m in moves(p):
            q = p + m
            futures.append(q)
    return len(longest.removeprefix(seed))
#assert walk('ihgpwlah') == 370
#assert walk('kglvqrro') == 492
#assert walk('ulqzkmiv') == 830

real_input = open('inputs/day17.input.txt').read().strip()
print(walk(real_input))  # => 392
