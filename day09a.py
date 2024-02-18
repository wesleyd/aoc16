#!/usr/bin/env python

def decompress(s):
    i = 0
    r = []
    while True: 
        j = s.find('(', i)
        if j < 0:
            r.append(s[i:])
            break
        r.append(s[i:j])
        x = s.find('x', j)
        k = s.find(')', x)
        l = int(s[j+1:x])
        n = int(s[x+1:k])
        r.extend([s[k+1:k+1+l]]*n)
        i = k+1+l
    return ''.join(r)

assert decompress('ADVENT') == 'ADVENT'
assert decompress('A(1x5)BC') == 'ABBBBBC'
assert decompress('(3x3)XYZ') == 'XYZXYZXYZ'
assert decompress('A(2x2)BCD(2x2)EFG') == 'ABCBCDEFEFG'
assert decompress('(6x1)(1x3)A') == '(1x3)A'
assert decompress('X(8x2)(3x3)ABCY') == 'X(3x3)ABC(3x3)ABCY'

real_input = open('inputs/day09.input.txt').read()
n = 0
for line in real_input.strip().splitlines():
    n += len(decompress(line))
print(n)
