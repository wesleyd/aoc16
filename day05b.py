#!/usr/bin/env python3

import hashlib

example_input = "abc"

def hash_hunt(s):
    i = 1
    while True:
        t = s + str(i)
        m = hashlib.md5(t.encode()).hexdigest()
        if m.startswith('00000'):
            yield (m[5], m[6])
        i += 1

def password(s):
    n = 0
    passwd = [None] * 8
    for pos, ch in hash_hunt(s):
        if pos not in '01234567':
            continue
        pos = int(pos)
        if passwd[pos] is not None:
            continue
        passwd[pos] = ch
        n += 1
        if n == 8:
            return ''.join(passwd)
# assert password(example_input) == '05ace8e3'

real_input = open('inputs/day05.input.txt').read().strip()
print(password(real_input)) # => 437e60fc
