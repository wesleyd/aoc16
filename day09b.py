#!/usr/bin/env python

def decompress(s):
    i = 0
    z = 0
    while True: 
        j = s.find('(', i)
        if j < 0:
            z += len(s) - i
            break
        z += j-i
        x = s.find('x', j)
        k = s.find(')', x)
        l = int(s[j+1:x])
        n = int(s[x+1:k])
        z += n * decompress(s[k+1:k+1+l])
        i = k+1+l
    return z

assert decompress('ADVENT') == 6
assert decompress('A(1x5)BC') == 7
assert decompress('(3x3)XYZ') == 9
assert decompress('X(8x2)(3x3)ABCY') == 20
assert decompress('(27x12)(20x12)(13x14)(7x10)(1x12)A') == 241920
assert decompress('(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN') == 445

real_input = open('inputs/day09.input.txt').read()
n = 0
for line in real_input.strip().splitlines():
    n += decompress(line)
print(n) # => 11052855125
