#!/usr/bin/env python3

import hashlib

from heapdict import heapdict

def moves(s):
    for c, d in zip(hashlib.md5(s.encode()).hexdigest()[:4], 'UDLR'):
        if c in 'bcdef':
            yield d
assert (l := ''.join(list(moves('hijkl')))) == 'UDL', l
assert (l := ''.join(list(moves('hijklD')))) == 'ULR', l
assert (l := ''.join(list(moves('hijklDR')))) == '', l
assert (l := ''.join(list(moves('hijklDU')))) == 'R', l
assert (l := ''.join(list(moves('hijklDUR')))) == '', l

def pos(s):
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
    futures = heapdict()
    futures[seed] = 0
    prev = {}
    while futures:
        p, dist = futures.popitem()
        for m in moves(p):
            q = p + m
            rc = pos(q)
            if not rc:
                continue
            if rc[0] == 3 and rc[1] == 3:
                return q.removeprefix(seed)
            futures[q] = dist+1

assert (p := walk('ihgpwlah')) == 'DDRRRD', p
assert (p := walk('kglvqrro')) == 'DDUDRLRRUDRD', p
assert (p := walk('ulqzkmiv')) == 'DRURDRUDDLLDLUURRDULRLDUUDDDRR', p

real_input = open('inputs/day17.input.txt').read().strip()
print(walk(real_input))  # => RDRRULDDDR
