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


def explore_map(map, x, y, steps, intersections, px, py):
    """ Explore the  map and record all intersections with their distances """

    if map[y][x] == '.' and y == len(map) - 1:
        intersections.append((y,x,py,px,steps))
        return
    map[y][x] = 'c'

    dx = [0,-1,0,1]
    dy = [1,0,-1,0]
    options = []
    for i in range(4):
        nx = x+dx[i]
        ny = y+dy[i]

        if nx < 0 or ny < 0 or nx >= len(map[0]) or ny >= len(map):
            continue
        # we cannot go through walls
        if map[ny][nx] == '#':
            continue
        # do not go back if the move would lead to the previous intersection
        if ny == py and nx == px:
            continue
        # do not go back, c is used to mark the previous spot
        if map[ny][nx] == 'c':
            map[ny][nx] = 'o'
            continue

        options.append((ny,nx))

    if len(options) == 0:
        map[y][x] = 'o'
    if len(options) > 1:
        intersections.append((y,x,py,px,steps))
        px = x
        py = y
        map[y][x] = 'x'
        steps = 0
    for o in options:
        # do not move somewhere we have already been
        if map[o[0]][o[1]] == 'o':
            continue
        nxt_steps = steps + 1
        ny, nx = o
        explore_map(map, nx, ny, nxt_steps, intersections, px, py)


def hike_nodes(nodes, pos, steps, visited, goal):
    visited.append(pos)

    if pos == goal:
        return steps

    max_steps = 0
    for nxt in nodes[pos]:
        nxt_pos = (nxt[0],nxt[1])
        if nxt_pos in visited:
            continue
        nxt_steps = steps + nxt[2]
        nxt_visited = deepcopy(visited)
        nxt_steps_taken = hike_nodes(nodes, nxt_pos, nxt_steps, nxt_visited, goal)
        max_steps = nxt_steps_taken if nxt_steps_taken > max_steps else max_steps

    return max_steps


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
    # Explore the map to reduce it to just intersections and their distances to each other
    intersections = []
    explore_map(map, x, y, 0, intersections, x, y)
    nodes = {}
    for i in intersections:
        nodes[(i[0],i[1])] = []
        nodes[(i[2],i[3])] = []
    for i in intersections:
        nodes[(i[0],i[1])].append((i[2],i[3],i[4]))
        nodes[(i[2],i[3])].append((i[0],i[1],i[4]))

    for i, p in enumerate(map[-1]):
        if p == '.':
            x = i
    print(hike_nodes(nodes, (0,1), 0, [], (len(map)-1, x)))

