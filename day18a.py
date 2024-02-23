#!/usr/bin/env python3

def next_line(s):
    t = []
    def at(i):
        if i < 0 or i >= len(s):
            return '.'
        return s[i]
    for i in range(len(s)):
        l, c, r = at(i-1), at(i), at(i+1)
        match (l, c, r):
            case ('^', '^', '.'):
                t.append('^')
            case ('.', '^', '^'):
                t.append('^')
            case ('^', '.', '.'):
                t.append('^')
            case ('.', '.', '^'):
                t.append('^')
            case _:
                t.append('.')
    return ''.join(t)
assert (nl := next_line('.^^^^')) == '^^..^', nl

example_input = """
.^^.^.^^^^
^^^...^..^
^.^^.^.^^.
..^^...^^^
.^^^^.^^.^
^^..^.^^..
^^^^..^^^.
^..^^^^.^^
.^^^..^.^^
^^.^^^..^^
""".strip()
example_lines = example_input.splitlines()
for i in range(len(example_lines)-1):
    assert (nl := next_line(example_lines[i])) == example_lines[i+1], (i, nl)

def count_safe_tiles(s, n):
    tot = 0
    while n:
        tot += s.count('.')
        n -= 1
        s = next_line(s)
    return tot

assert (t := count_safe_tiles('.^^.^.^^^^', 10)) == 38, t

real_input = open('inputs/day18.input.txt').read().strip()
print(count_safe_tiles(real_input, 40))  # => 1961
