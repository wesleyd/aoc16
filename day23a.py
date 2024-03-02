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

def tgl(ram, pc, x):
    if pc+x < 0 or len(ram) <= pc+x:
        print ('attempt made to toggle instruction out of program '
              f'@ram[{pc=}]={ram[pc]}: {pc+x=} not in [0,{len(ram)=}]')
        return
    #print(f'tgl {x}: ram[{pc+x=}]={ram[pc+x]} => ', end='')
    if len(ram[pc+x]) == 2:
        if ram[pc+x][0] == 'inc':
            ram[pc+x][0] = 'dec'
        else:
            ram[pc+x][0] = 'inc'
    elif len(ram[pc+x]) == 3:
        if ram[pc+x][0] == 'jnz':
            ram[pc+x][0] = 'cpy'
        else:
            ram[pc+x][0] = 'jnz'
    else:
        assert False, f'weird instr at {pc+x=}: {ram[pc+x]=}'
    #print(f'{ram[pc+x]}')

class CPU(object):
    def __init__(self, inp):
        self.registers = {'a': 7, 'b': 0, 'c': 0, 'd': 0}
        self.ram = [line.split() for line in inp.strip().splitlines()]
        self.pc = 0
    def lookup(self, op):
        if op in 'abcd':
            return self.registers[op]
        return int(op)
    def print(self):
        rr = 'abcd'
        tab = 20 
        for i, instr in enumerate(self.ram):
            if i == self.pc:
                line = '=> '
            else:
                line = '   '
            line += ' '.join(instr)
            print(line, end='')
            if i < 4:
                r = rr[i]
                print(' '*(tab - len(line)), f'{r}={self.registers[r]}')
            else:
                print()
        print()

def step1(cpu):
    cpu = copy.deepcopy(cpu)
    match cpu.ram[cpu.pc]:
        case ['cpy', src, dst]:
            cpu.registers[dst] = cpu.lookup(src)
        case ['inc', r]:
            cpu.registers[r] += 1
        case ['dec', r]:
            cpu.registers[r] -= 1
        case ['jnz', r, o]:
            if cpu.lookup(r) != 0:
                cpu.pc += cpu.lookup(o)-1
        case ['tgl', x]:
            tgl(cpu.ram, cpu.pc, cpu.lookup(x))
        case _:
            assert False, ram[pc]
    cpu.pc += 1
    return cpu


def run(inp):
    cpu = CPU(inp)
    #cpu.print()
    #n = 0
    while 0 <= cpu.pc < len(cpu.ram):
        #if n:
        #    n -= 1
        #else:
        #    x = sys.stdin.readline()
        #    try:
        #        n = int(x)
        #    except ValueError:
        #        pass
        cpu = step1(cpu)
        #if not n or cpu.pc > 14:
        #    cpu.print()
    #cpu.print()
    return cpu.registers['a']

#assert run(example_input) == 3

real_input = open('inputs/day23.input.txt').read()
print(run(real_input))  # 318020 is too high
