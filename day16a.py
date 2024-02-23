#!/usr/bin/env python3

def dragon(a):
    inv = { '0': '1', '1': '0' }
    b = ['0']
    for c in reversed(a):
        b.append(inv[c])
    return a + ''.join(b)
assert (d := dragon('1')) == '100', d
assert (d := dragon('0')) == '001', d
assert (d := dragon('11111')) == '11111000000', d
assert (d := dragon('111100001010')) == '1111000010100101011110000', d
real_input = open('inputs/day16.input.txt').read()

def checksum1(s):
    assert len(s) % 2 == 0, len(s)
    cs = []
    for i in range(0, len(s)-1, 2):
        if s[i] == s[i+1]:
            cs.append('1')
        else:
            cs.append('0')
    return ''.join(cs)
assert (c := checksum1('10000011110010000111')) == '0111110101', c

def checksum(s):
    while True:
        s = checksum1(s)
        if len(s) % 2 == 1:
            return s
assert (c := checksum('10000011110010000111')) == "01100", c

def csfill(seed, length):
    s = seed
    while len(s) < length:
        s = dragon(s)
    s = s[:length]
    return checksum(s)
assert (c := csfill('10000', 20)) == '01100', c

real_input = open('inputs/day16.input.txt').read().strip()
print(csfill(real_input, 272)) # => 10010100110011100
