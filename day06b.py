#!/usr/bin/env python3

from collections import defaultdict

example_input = """
eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar
"""

def histoify(inp):
    msgs = inp.strip().splitlines()
    histos = [defaultdict(int) for _ in range(len(msgs[0]))] 
    for line in inp.strip().splitlines():
        for i, ch in enumerate(line):
            histos[i][ch] += 1
    decoded = []
    for i, histo in enumerate(histos):
        decoded.append(min(histo, key=lambda ch: histo[ch]))
    return ''.join(decoded)
assert histoify(example_input) == 'advent'

real_input = open('inputs/day06.input.txt').read()
print(histoify(real_input)) # => pdesmnoz
