#!/usr/bin/env python3

import itertools

def netsplit(s):
    inside = False
    supernets, hypernets = [], []
    i = 0
    j = i
    while j < len(s):
        j += 1
        if j == len(s) or not s[j].isalpha():
            if inside:
                hypernets.append(s[i:j])
            else:
                supernets.append(s[i:j])
            inside = not inside
            i = j+1
            j = i
    return supernets, hypernets
assert netsplit('zazbz[bzb]cdb') == (['zazbz', 'cdb'], ['bzb'])
assert netsplit('zhrh[xda]bgf[rlcx]ybts') == (['zhrh', 'bgf', 'ybts'], ['xda', 'rlcx'])

def empty(it):
    """True if it was empty."""
    for _ in it:
        return False
    return True

def abas(s):
    """Yields all the ABAs in s."""
    if isinstance(s, list):
        for t in s:
            yield from abas(t)
    for i in range(len(s)-2):
        if s[i] == s[i+2] and s[i] != s[i+1]:
            yield s[i:i+3]
assert list(abas('hgyghg')) == ['gyg', 'ghg']
assert list(abas(['aba', 'bab'])) == ['aba', 'bab']

def ssl(s):
    sn, hn = netsplit(s)
    babs = set(abas(hn))
    for aba in abas(sn):
        bab = aba[1] + aba[0] + aba[1]
        if bab in babs:
            return True
    return False
assert ssl('aba[bab]xyz')
assert not ssl('xyx[xyx]xyx')
assert ssl('aaa[kek]eke')
assert ssl('zazbz[bzb]cdb')

real_input = open('inputs/day07.input.txt').read()

def count(inp):
    n = 0
    for line in inp.strip().splitlines():
        #print(line)
        if ssl(line):
            n += 1
    return n

print(count(real_input))  # => 258
