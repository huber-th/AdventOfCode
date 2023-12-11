# setting path
""" filesystem paths module """
from pathlib import Path


def load_data(file: str):
    """ Load and sanitize data """
    p = Path(__file__).with_name(file)
    with p.open('r', encoding='utf8') as f:
        c = f.read().strip().split('\n')
    return c


def next_position(rows: [str], curr: (str, int, int), direction: str) -> (int, int, str):
    """ 
    Find the next position given the current pipe part and direction
    """
    if curr[0] == 'F':
        if direction == 'R':
            nxt = (rows[curr[1]][curr[2]+1], curr[1], curr[2]+1)
        if direction == 'D':
            nxt = (rows[curr[1]+1][curr[2]], curr[1]+1, curr[2])
    if curr[0] == '-':
        if direction == 'R':
            nxt = (rows[curr[1]][curr[2]+1], curr[1], curr[2]+1)
        if direction == 'L':
            nxt = (rows[curr[1]][curr[2]-1], curr[1], curr[2]-1)
    if curr[0] == '7':
        if direction == 'D':
            nxt = (rows[curr[1]+1][curr[2]], curr[1]+1, curr[2])
        if direction == 'L':
            nxt = (rows[curr[1]][curr[2]-1], curr[1], curr[2]-1)
    if curr[0] == '|':
        if direction == 'U':
            nxt = (rows[curr[1]-1][curr[2]], curr[1]-1, curr[2])
        if direction == 'D':
            nxt = (rows[curr[1]+1][curr[2]], curr[1]+1, curr[2])
    if curr[0] == 'J':
        if direction == 'U':
            nxt = (rows[curr[1]-1][curr[2]], curr[1]-1, curr[2])
        if direction == 'L':
            nxt = (rows[curr[1]][curr[2]-1], curr[1], curr[2]-1)
    if curr[0] == 'L':
        if direction == 'U':
            nxt = (rows[curr[1]-1][curr[2]], curr[1]-1, curr[2])
        if direction == 'R':
            nxt = (rows[curr[1]][curr[2]+1], curr[1], curr[2]+1)
    return nxt


def next_direction(part: str, prev: str) -> str:
    """ Determine first step for a pipe """
    if part == 'F':
        return 'D' if prev == 'L' else 'R'
    if part == '-':
        return 'L' if prev == 'L' else 'R'
    if part == '7':
        return 'L' if prev == 'U' else 'D'
    if part == '|':
        return 'U' if prev == 'U' else 'D'
    if part == 'J':
        return 'U' if prev == 'R' else 'L'
    if part == 'L':
        return 'R' if prev == 'D' else 'U'
    return ''


def find_loop_length(rows: [str]) -> int:
    """ Find the loop and return it's length """
    max_length = 0
    curr = start = ('|', 19, 88)
    step = 'U'
    length = 0
    row_tiles = {19: [88]}
    while True:
        nxt = next_position(rows, curr, step)
        length += 1
        if nxt[1] == start[1] and nxt[2] == start[2]:
            if length > max_length:
                max_length = length
            break
        step = next_direction(nxt[0], step)
        curr = nxt
        tile = row_tiles.get(curr[1], [])
        tile.append(curr[2])
        row_tiles[curr[1]] = tile

    # Build a map of the loop for part 2
    loop_map = []
    row_tiles = dict(sorted(row_tiles.items()))
    for row in row_tiles.items():
        loop_map_row = []
        for i in range(0, len(rows[0])):
            loop_map_row.append(rows[row[0]][i] if i in row[1] else '.')
        loop_map.append(loop_map_row)
    return (max_length, loop_map)


def get_x_y_from_curr(curr: (str, int, int), direction: str) -> (int, int):
    """ Get the x,y coordinates to check for flood fill """
    if curr[0] == '|' and direction == "D":
        return curr[1], curr[2]+1
    if curr[0] == '|' and direction == "U":
        return curr[1], curr[2]-1
    if curr[0] == '-' and direction == "L":
        return curr[1]+1, curr[2]
    if curr[0] == '-' and direction == "R":
        return curr[1]-1, curr[2]
    return -1, -1


def flood_recursive(x, y, flood_map, depth: int) -> int:
    """ Fill enclosed tiles with 'I' """
    # Check for map boundaries and stop if we step beyond the 2d world
    if x < 0 or y < 0 or x >= len(flood_map) or y >= len(flood_map[0]):
        return 0
    # if the spot is not a '.' we do not need to continue
    # it's either part of the loop or already marked
    if flood_map[x][y] != '.':
        return 0
    # update the color of the current square to the replacement color
    print(f'Marking {x}:{y} as enclosed')
    flood_map[x][y] = 'I'
    count = 1
    neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    for n in neighbors:
        next_depth = depth + 1
        count += flood_recursive(n[0], n[1], flood_map, next_depth)
    return count


if __name__ == '__main__':
    data = load_data('input')

    print('Part one:')
    result = find_loop_length(data)
    print(result[0]/2)

    print('Part two:')
