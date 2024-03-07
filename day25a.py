#!/usr/bin/env python3

from itertools import islice

class CPU(object):
    def __init__(self, inp):
        self.ram = [line.split() for line in inp.strip().splitlines()]
        self.optimize()
        self.reset()
    def reset(self):
        self.registers = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
        self.pc = 0
    def lookup(self, op):
        if op in 'abcd':
            return self.registers[op]
        return int(op)
    def optimize(self):
        for i in range(len(self.ram)-6):
            match self.ram[i:i+6]:
                case ( ('cpy', X, Y),
                    ('inc', W),
                    ('dec', Y2),
                    ('jnz', Y3, '-2'),
                    ('dec', Z),
                    ('jnz', Z2, '-5') ) if (
                        Y == Y2 == Y3 and Z == Z2 and
                        len(set([W,X,Y,Z])) == 4) :
                    self.ram[i] = ['addmul', W, X, Z]  # W += X*Z
                    self.ram[i+1] = ['cpy', Y, 0]
                    self.ram[i+2] = ['cpy', Z, 0]
                    self.ram[i+3] = ['pass']
                    self.ram[i+4] = ['pass']
                    self.ram[i+5] = ['pass']
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
            case['out', r]:
                yield self.lookup(r)
            case _:
                assert False, ram[pc]
        self.pc += 1
    def clock(self, a):
        """Yields the clock seeded with a."""
        self.reset()
        self.registers['a'] = a
        while 0 <= self.pc < len(self.ram):
            yield from self.step()

def wants():
    """Yield perfect clock signal."""
    while True:
        yield 0
        yield 1

def diverges(cpu, a, n=1000):
    """Returns the index at which a's clock diverges, or n if it doesn't."""
    for want, got, i in zip(wants(), cpu.clock(a), range(n)):
        if got != want:
            #print(f'{a} failed at {i}')
            return i
    return n

def run(inp):
    cpu = CPU(inp)
    lim = 100
    a = 0
    while True:
        d = diverges(cpu, a, lim)
        #print(f'{a=} diverges at {d=}')
        if d == lim:
            return a
        if d*3 > lim:
            lim = d*3
        a += 1

real_input = open('inputs/day25.input.txt').read()
print(run(real_input))  # => 175
