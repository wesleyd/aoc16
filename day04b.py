#!/usr/bin/env python

def parse(inp):
    rooms = []
    for line in inp.strip().splitlines():
        interesting = line.split('[')[0]
        pieces = interesting.split('-')
        encrypted_name = ' '.join(pieces[:-1])
        sector_id = int(pieces[-1])
        rooms.append((encrypted_name, sector_id))
    return rooms

def decrypt(encrypted_name, sector_id):
    t = []
    for c in encrypted_name:
        n = ord(c) - ord('a')
        if n < 0 or 26 <= n:
            t.append(' ')
            continue
        n += sector_id % 26
        n %= 26
        t.append(chr(n + ord('a')))
    return ''.join(t)
assert decrypt('qzmt-zixmtkozy-ivhz', 343) == 'very encrypted name'

real_input = open('inputs/day04.input.txt').read()
for encrypted_name, sector_id in parse(real_input):
    name = decrypt(encrypted_name, sector_id)
    if name == 'northpole object storage':
        print(sector_id)  # => 993
    
