#!/usr/bin/env python3

import re

from collections import defaultdict
from dataclasses import dataclass, field

def extract_numbers(s):
    for n in re.findall(r'\d+', s):
       yield int(n) 

@dataclass(repr=True)
class Bot:
    low: int  = ('', -1)
    high: int = ('', -1)
    has: list[int] = field(default_factory=list)
    output: int = -1
    
class Machine:
    def __init__(self, inp):
        self.bots = defaultdict(Bot)
        for line in inp.strip().splitlines():
            m = re.match('bot (\d+) gives low to (output|bot) (\d+) and high to (output|bot) (\d+)', line)
            if m:
                b = int(m.group(1))
                l = (m.group(2), int(m.group(3)))
                h = (m.group(4), int(m.group(5)))
                self.bots[b].low = l
                self.bots[b].high = h
            elif line.startswith('value'):
                v, b = extract_numbers(line)
                self.bots[b].has.append(v)
            else:
                assert False, f'Bad line "{line}"'
    def __str__(self):
        return f'Machine({self.bots})'
    def send(self, to, value):
        dest, b = to
        if dest == 'output':
            self.bots[b].output = value
        elif dest == 'bot':
            self.bots[b].has.append(value)
        else:
            assert False, (to, value)
    def run(self, goal=None):
        finished = False
        while not finished:
            finished = True
            for b, bot in self.bots.items():
                if len(bot.has) > 1:
                    finished = False
                    bot.has.sort()
                    if goal and sorted(goal) == bot.has:
                        return b
                    self.send(bot.low, bot.has[0])
                    self.send(bot.high, bot.has[1])
                    bot.has = []

real_input = open('inputs/day10.input.txt').read()
m = Machine(real_input)
m.run()
print(m.bots[0].output * m.bots[1].output * m.bots[2].output) # => 3965
