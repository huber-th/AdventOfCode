import math

from pathlib import Path

input = {}
input_instructions = ""

def follow_map(guide: str, map) -> int:
     pos = "AAA"
     idx = 0
     while pos != "ZZZ":
         d = guide[idx%len(guide)]
         pos = map[pos][0 if d=='L' else 1]
         idx += 1
     return idx

def follow(start):
    pos = start
    idx = 0
    while not pos.endswith('Z'):
     d = input_instructions[idx%len(input_instructions)]
     pos = input[pos][0 if d=='L' else 1]
     idx += 1
    return idx


p = Path(__file__).with_name('input')
with p.open('r') as f:
    input_instructions, m = f.read().strip().split('\n\n')
    map = m.split('\n')
    input = {}
    for m in map:
        pos, next = m.split(' = ')
        input[pos] = next.replace('(','').replace(')','').replace(' ','').split(',')

    print('Part one:')
    print(follow_map(input_instructions, input))
    print('Part two:')
    steps = 1
    for s in input.keys():
     if s.endswith('A'):
         steps = math.lcm(steps, follow(s))
    print(steps)        
 