#!/usr/bin/env python3

import copy
import sys

from collections import defaultdict

example_input = """
cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a
"""

def optimize(rom):
    ram = rom[:]
    for i in range(len(rom)-6):
        match rom[i:i+6]:
            case ( ('cpy', X, Y),
                   ('inc', W),
                   ('dec', Y2),
                   ('jnz', Y3, '-2'),
                   ('dec', Z),
                   ('jnz', Z2, '-5') ) if (
                       Y == Y2 == Y3 and Z == Z2 and
                       len(set([W,X,Y,Z])) == 4) :
                ram[i] = ['addmul', W, X, Z]  # W += X*Z
                ram[i+1] = ['cpy', Y, 0]
                ram[i+2] = ['cpy', Z, 0]
                ram[i+3] = ['pass']
                ram[i+4] = ['pass']
                ram[i+5] = ['pass']
                #print(f'Modified: {rom[i:i+6]} -> {ram[i:i+6]}')
    return ram
                          
class CPU(object):
    def __init__(self, inp):
        self.registers = {'a': 12, 'b': 0, 'c': 0, 'd': 0}
        self.rom = [line.split() for line in inp.strip().splitlines()]
        self.ram = optimize(self.rom)
        self.pc = 0
    def lookup(self, op):
        if op in 'abcd':
            return self.registers[op]
        return int(op)
    def step(self):
        match self.ram[self.pc]:
            case ['cpy', src, dst]:
                self.registers[dst] = self.lookup(src)
            case ['inc', r]:
                self.registers[r] += 1
            case ['dec', r]:
                self.registers[r] -= 1
            case ['jnz', r, o]:
                if self.lookup(r) != 0:
                    self.pc += self.lookup(o)-1
            case ['pass', *_]:
                pass
            case ['addmul', W, X, Z]:
                assert W != X and X != Z and W != Z, (W, X, Z)
                self.registers[W] += self.lookup(X) * self.lookup(Z)
            case ['tgl', x]:
                p = self.pc + self.lookup(x)
                if 0 <= p < len(self.rom):
                    if len(self.rom[p]) == 2:
                        if self.rom[p][0] == 'inc':
                            self.rom[p][0] = 'dec'
                        else:
                            self.rom[p][0] = 'inc'
                    elif len(self.rom[p]) == 3:
                        if self.rom[p][0] == 'jnz':
                            self.rom[p][0] = 'cpy'
                        else:
                            self.rom[p][0] = 'jnz'
                    else:
                        assert False, f'self.rom[{p=}]={self.rom[p]}'
                    self.ram = optimize(self.ram)
                else:
                    #print(f'tgl out of range {p=}')
                    pass
                pass
            case _:
                assert False, ram[pc]
        self.pc += 1

def run(inp, a):
    cpu = CPU(inp)
    cpu.registers['a'] = a
    while 0 <= cpu.pc < len(cpu.ram):
        cpu.step()
    return cpu.registers['a']

assert run(example_input, 2) == 3

real_input = open('inputs/day23.input.txt').read()
assert run(real_input, 7) == 12860
print(run(real_input, 12))  # => 479009420
