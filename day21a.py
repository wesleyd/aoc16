#!/usr/bin/env python3

example_input = """
swap position 4 with position 0
swap letter d with letter b
reverse positions 0 through 4
rotate left 1 step
move position 1 to position 4
move position 3 to position 0
rotate based on position of letter b
rotate based on position of letter d
"""
example_rules = example_input.strip().splitlines()

def scramble(rules, password):
    s = list(password)
    for rule in rules:
        match rule.split(' '):
            case ['swap', 'position', X, 'with', 'position', Y]:
                X, Y = int(X), int(Y)
                s[X], s[Y] = s[Y], s[X]
            case ['swap', 'letter', A, 'with', 'letter', B]:
                X, Y = s.index(A), s.index(B)
                s[X], s[Y] = s[Y], s[X]
            case ['rotate', dirn, X, 'step'|'steps']:
                assert dirn in ('left', 'right'), dirn
                X = int(X) * (-1 if dirn == 'right' else 1)
                s = s[X:] + s[:X]
            case ['reverse', 'positions', X, 'through', Y]:
                X, Y = int(X), int(Y)
                s = s[:X] + list(reversed(s[X:Y+1])) + s[Y+1:]
            case ['move', 'position', X, 'to', 'position', Y]:
                X, Y = int(X), int(Y)
                c = s.pop(X)
                s.insert(Y, c)
            case ['rotate', 'based', 'on', 'position', 'of', 'letter', C]:
                X = s.index(C)
                X += 1 + (1 if X >=4 else 0)
                while X:
                    s = s[-1:] + s[:-1]
                    X -= 1
            case _:
                pass
    return ''.join(s)
assert scramble(example_rules, 'abcde') == 'decab'

real_input = open('inputs/day21.input.txt').read()
real_rules = real_input.strip().splitlines()
print(scramble(real_rules, 'abcdefgh'))  # => fdhbcgea
