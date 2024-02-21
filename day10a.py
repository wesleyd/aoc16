#!/usr/bin/env python3

import re

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict

example_input = """
value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2
"""

def extract_numbers(s):
    for n in re.findall(r'\d+', s):
       yield int(n) 

@dataclass(repr=True)
class Bot:
    low:int  = -1
    high: int = -1
    has: list[int] = field(default_factory=list)
    output: int = -1
    
class Machine:
    def __init__(self, inp):
        self.bots = defaultdict(Bot)
        for line in inp.strip().splitlines():
            if line.startswith('value'):
                v, b = extract_numbers(line)
                self.bots[b].has.append(v)
            elif line.startswith('bot'):
                b, l, h = extract_numbers(line)
                self.bots[b].low = l
                self.bots[b].high = h
    def __str__(self):
        return f'Machine({self.bots})'
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
                    if bot.low == b:
                        bot.output = bot.has[0]
                    else:
                        self.bots[bot.low].has.append(bot.has[0])
                    if bot.high == b:
                        bot.output = bot.has[1]
                    else:
                        self.bots[bot.high].has.append(bot.has[1])
                    bot.has = []

#m = Machine(example_input)
#m.run()

real_input = open('inputs/day10.input.txt').read()
print(Machine(real_input).run([17, 61]))  # => 73
