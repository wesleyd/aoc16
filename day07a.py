#!/usr/bin/env python3

import re

def abba(s):
    mm = re.search(r'([a-z])([a-z])\2\1', s)
    return mm and mm.group(1) != mm.group(2)

def tls(s):
    hypernets = re.findall(r'\[[a-z]+\]', s)
    for hn in hypernets:
        if abba(hn):
            return False
        s = s.replace(hn, '-', 1) 
    for t in s.split('-'):
        if abba(t):
            return True
    return False

assert tls('abba[mnop]qrst')
assert not tls('abcd[bddb]xyyx')
assert not tls('aaaa[qwer]tyui')
assert tls('ioxxoj[asdfgh]zxcvbn')

real_input = open('inputs/day07.input.txt').read()

def count(inp):
    n = 0
    for line in inp.strip().splitlines():
        #print(line)
        if tls(line):
            n += 1
    return n

print(count(real_input))  # => 105
