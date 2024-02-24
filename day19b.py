#!/usr/bin/env python3

def run(n):
    elves = [1] * n
    def next_elf(i):
        while True:
            i = i + 1 if i < len(elves)-1 else 0
            if elves[i] > 0:
                return i
    i = 0
    o = n//2
    while n > 1:
        assert elves[o] > 0, o
        elves[i] += elves[o]
        elves[o] = 0
        n -= 1
        i = next_elf(i)
        o = next_elf(o)
        if n % 2 == 0:
            o = next_elf(o)
    for i, gifts in enumerate(elves):
        if gifts > 0:
            return i+1

assert run(5) == 2

real_input = int(open('inputs/day19.input.txt').read())
print(run(real_input))  # => 1424135
