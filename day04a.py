#!/usr/bin/env python

from collections import defaultdict, namedtuple

example_input = """
aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]
"""

Room = namedtuple('Room', ['encrypted_name', 'sector_id', 'checksum'])

def parse(inp):
    rooms = []
    for line in inp.strip().splitlines():
        pieces = line.split('-')
        encrypted_name = ''.join(pieces[:-1])
        trailers = pieces[-1].split('[')
        sector_id = int(trailers[0])
        checksum = trailers[1][:-1]
        rooms.append(Room(encrypted_name, int(sector_id), checksum))
    return rooms
example_rooms = parse(example_input)

def common5(s):
    histo = defaultdict(int)
    for c in s:
        histo[c] += 1
    counts = defaultdict(list)
    for c, n in histo.items():
        counts[n].append(c)
    s = []
    for n in sorted(counts, reverse=True):
        s.extend(sorted(counts[n]))
        if len(s) >= 5:
            return ''.join(s[:5])
    
def sector_id_sum(rooms):
    n = 0
    for room in rooms:
        checksum = common5(room.encrypted_name)
        if checksum == room.checksum:
            n += room.sector_id
    return n

assert sector_id_sum(example_rooms) == 1514

real_input = open('inputs/day04.input.txt').read()
real_rooms = parse(real_input)
print(sector_id_sum(real_rooms))  # => 158835
