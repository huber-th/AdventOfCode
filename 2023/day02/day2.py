from pathlib import Path
import re

input = []

p = Path(__file__).with_name('input')
with p.open('r') as f:
    lines = f.read().split('\n')
    for l in lines:
        prefix, game = l.replace('; ', ';').split(':')
        input.append(game.strip().replace(', ', ','))

def verifyGame(games):
    for d in games:
        blocks = d.split(',')
        for b in blocks:
            colour = b.split(' ')
            if colour[1] == 'red' and int(colour[0]) > 12:
                return False
            if colour[1] == 'green' and int(colour[0]) > 13:
                return False
            if colour[1] == 'blue' and int(colour[0]) > 14:
                return False
    return True

sum = 0
for i,s in enumerate(input):
    games = s.split(';')

    if verifyGame(games):
        sum += i+1

print('Part one:')
print(sum)

sum = 0

def findMinCubesPossible(draws):
    r=0
    g=0
    b=0
    for d in draws:
        blocks = d.split(',')
        for bl in blocks:
            colour = bl.split(' ')
            if colour[1] == 'red':
                if int(colour[0]) > r:
                    r = int(colour[0])
            if colour[1] == 'green':
                if int(colour[0]) > g:
                    g = int(colour[0])
            if colour[1] == 'blue':
                if int(colour[0]) > b:
                    b = int(colour[0])
    return [r,g,b]

for i,s in enumerate(input):
    draws = s.split(';')
    cubes = findMinCubesPossible(draws)
    power = int(cubes[0])*int(cubes[1])*int(cubes[2])
    sum += power

print('Part two:')
print(sum)
    
