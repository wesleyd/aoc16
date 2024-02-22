#!/usr/bin/env python3

from collections import defaultdict

example_input = """
cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a
"""

def run(inp):
    registers = defaultdict(int)
    registers['c'] = 1
    def lookup(op):
        if op in 'abcd':
            return registers[op]
        return int(op)
    lines = inp.strip().splitlines()
    pc = 0
    while 0 <= pc < len(lines):
        match lines[pc].split():
            case ['cpy', src, dst]:
                registers[dst] = lookup(src)
            case ['inc', r]:
                registers[r] += 1
            case ['dec', r]:
                registers[r] -= 1
            case ['jnz', r, o]:
                if lookup(r) != 0:
                    pc += int(o)-1
            case _:
                assert False, lines[pc]
        pc += 1
    return registers['a']
assert run(example_input) == 42

real_input = open('inputs/day12.input.txt').read()
print(run(real_input))  # => 9227674
