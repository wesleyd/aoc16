#!/usr/bin/env python3

import hashlib
import re

from functools import cache

example_input = 'abc'

triple = re.compile(r'(.)\1\1')

class Hasher(object):
    def __init__(self, salt):
        self.salt = salt
        self.hashes = {}
        self.keys = []
    @cache
    def hash(self, n):
        h = self.salt + str(n)
        for i in range(2017):
            h = hashlib.md5(h.encode()).hexdigest()
        return h
    def is_key(self, n):
        if not (m := triple.search(self.hash(n))):
            return False
        x5 = m.group(1)*5
        for i in range(1000):
            if x5 in self.hash(n+i+1):
                return True
        return False
    def next_key(self):
        if not self.keys:
            k = 0
        else:
            k = self.keys[-1]
        while True:
            k += 1
            if self.is_key(k):
                self.keys.append(k)
                return k
    def nth_key(self, n):
        while len(self.keys) < n:
            self.next_key()
        return self.keys[n-1]

example_hasher = Hasher(example_input)
assert (k := example_hasher.nth_key(1)) == 10, k
assert (k := example_hasher.nth_key(64)) == 22551, k

real_input = open('inputs/day14.input.txt').read().strip()
real_hasher = Hasher(real_input)
print(real_hasher.nth_key(64))  # => 22045
