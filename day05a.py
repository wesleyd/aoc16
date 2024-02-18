#!/usr/bin/env python3

import hashlib
import itertools

example_input = "abc"

def hash_hunt(s):
    i = 1
    while True:
        t = s + str(i)
        m = hashlib.md5(t.encode()).hexdigest()
        if m.startswith('00000'):
            #print(t, m, i, m[5])
            yield m[5]
        i += 1

def password(s):
    return ''.join(itertools.islice(hash_hunt(s), 8))
assert password(example_input) == '18f47a30'

real_input = open('inputs/day05.input.txt').read().strip()

print(password(real_input)) # => 2414bc77
