#!/usr/bin/env python3

def run(n):
    elves = {i: 1 for i in range(n)}
    def inc(i):
        return i+1 if i < n-1 else 0
    i = 0
    while len(elves) > 1:
        j = inc(i)
        while j not in elves:
            j = inc(j)
        elves[i] += elves[j]
        del elves[j]
        i = inc(i)
        while i not in elves:
            i = inc(i)
    assert len(elves) == 1, elves
    for i in elves:
        return i+1

assert run(5) == 3

real_input = int(open('inputs/day19.input.txt').read())
print(run(real_input))  # => 1842613
