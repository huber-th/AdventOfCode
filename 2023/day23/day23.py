""" filesystem paths module """
from pathlib import Path
from copy import deepcopy
import sys
sys.setrecursionlimit(100000)

def load_data(file: str):
    """ Load and sanitize data """
    p = Path(__file__).with_name(file)
    with p.open('r', encoding='utf8') as f:
        c = f.read().strip().split('\n')
        d = []
        for l in c:
            line = []
            for p in l:
                line.append(p)
            d.append(line)
    return d


def hike_the_scenic_route(map, x, y, steps, visited):
    """ Hike and find the longest possible way """
    visited.append((y,x))

    if map[y][x] == '.' and y == len(map) - 1:
        return steps

    next_steps = steps + 1

    dx = [0,-1,0,1]
    dy = [1,0,-1,0]
    result = 0
    for i in range(4):
        nx = x+dx[i]
        ny = y+dy[i]
        if (ny,nx) in visited:
            continue

        if nx < 0 or ny < 0 or nx >= len(map[0]) or ny >= len(map):
            continue
        # Can we move into the direction?
        if map[ny][nx] == '#':
            continue
        # Ensure on ice we only go into that direction
        if map[y][x] == '<' and i != 1:
            continue
        if map[y][x] == '>' and i != 3:
            continue
        if map[y][x] == 'v' and i != 0:
            continue

        next_visited = deepcopy(visited)
        length = hike_the_scenic_route(map, nx, ny, next_steps, next_visited)
        if length > result:
            result = length
    return result


if __name__ == '__main__':
    map = load_data('input')

    print('Part one:')
    x = None
    y = 0
    for i, p in enumerate(map[0]):
        if p == '.':
            x = i
    print(hike_the_scenic_route(map, x, y, 0, []))

    print('Part two:')
