#!/usr/bin/env python3

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
        #print ('attempt made to toggle instruction out of program '
        #      f'@ram[{pc=}]={ram[pc]}: {pc+x=} not in [0,{len(ram)=}]')
        return
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

class CPU(object):
    def __init__(self, inp):
        self.registers = {'a': 7, 'b': 0, 'c': 0, 'd': 0}
        self.ram = [line.split() for line in inp.strip().splitlines()]
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
            case ['tgl', x]:
                tgl(self.ram, self.pc, self.lookup(x))
            case _:
                assert False, (pc, registers, ram[self.pc])
        self.pc += 1
    def run(self):
        while 0 <= self.pc < len(self.ram):
            self.step()
        return self.registers['a']

real_input = open('inputs/day23.input.txt').read()
print(CPU(real_input).run())  # => 12860
