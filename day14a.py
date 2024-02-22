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
        s = self.salt + str(n)
        return hashlib.md5(s.encode()).hexdigest()
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
assert (n := example_hasher.next_key()) == 39, n
assert (n := example_hasher.next_key()) == 92, n
assert (k := example_hasher.nth_key(64)) == 22728, k

real_input = open('inputs/day14.input.txt').read().strip()
real_hasher = Hasher(real_input)
print(real_hasher.nth_key(64))  # => 25427
