""" Advent of Code 2024 """
from pathlib import Path
from copy import deepcopy


def load_data():
    """
    Load and sanitize data

    Return: The loaded and sanitized file content for processing
    """
    p = Path(__file__).with_name('input')
    with p.open('r', encoding='utf8') as f:
        c = [list(line) for line in f.read().strip().split('\n')]

    return c


def find_start(map):
    """ Find the starting position marked with ^ """
    for y, row in enumerate(map):
        for x, char in enumerate(row):
            if char == '^':
                return (y, x)


def next_position(curr, dir):
    """ Calculate the next position based on direction U, R, D, L """
    next = [0, 0]
    if dir == 'U':
        next[0] = curr[0] - 1
        next[1] = curr[1]
    elif dir == 'R':
        next[0] = curr[0]
        next[1] = curr[1] + 1
    elif dir == 'D':
        next[0] = curr[0] + 1
        next[1] = curr[1]
    elif dir == 'L':
        next[0] = curr[0]
        next[1] = curr[1] - 1

    return next


def move(map, curr, dir):
    """ Move one step on the map from curr into direction dir """
    next = next_position(curr, dir)
    # If the next position is blocked, which is marked by #, turn right

    if (next[0] < 0 or
            next[0] >= len(map) or
            next[1] < 0 or
            next[1] >= len(map[0])):
        return next, dir

    while map[next[0]][next[1]] == '#':
        if dir == 'U':
            dir = 'R'
        elif dir == 'R':
            dir = 'D'
        elif dir == 'D':
            dir = 'L'
        elif dir == 'L':
            dir = 'U'
        next = next_position(curr, dir)

    map[next[0]][next[1]] = 'X'
    # print_map(map)
    # input()
    return next, dir


def print_map(map):
    """ Print the map for debugging """
    for row in map:
        print(row)


def navigate_map(map, curr, dir) -> bool:
    """
    Start navigating the map until we leave the map

    Returns: True if a loop was detected, false otherwise
    """
    curr, dir = move(map, curr, dir)

    # Keep track of visited tiles and their direction to find loops
    visited = set()

    while (curr[0] >= 0 and
           curr[1] >= 0 and
           curr[0] < len(map) and
           curr[1] < len(map[0])):
        curr, dir = move(map, curr, dir)
        if (curr[0], curr[1], dir) in visited:
            return True
        visited.add((curr[0], curr[1], dir))
    return False


def visited_tiles(map):
    """ Find tiles visited marked by X """
    tiles = []
    for y, row in enumerate(map):
        for x, tile in enumerate(row):
            if tile == 'X':
                tiles.append((y, x))
    return tiles


def part_one():
    """ Solution Implementation for Part 1 """
    map = load_data()

    print('Part one:')
    start = find_start(map)
    map[start[0]][start[1]] = 'X'
    navigate_map(map, start, 'U')
    print(len(visited_tiles(map)))
    return map


def part_two():
    """ Solution Implementation for Part 2 """
    map = load_data()

    print('Part two:')

    # Run part one again to find all visited so we don't have to try every spot
    start = find_start(map)
    map[start[0]][start[1]] = 'X'
    original = deepcopy(map)
    navigate_map(map, start, 'U')
    visited = visited_tiles(map)

    # Remove the start since we can't block it
    visited.remove(start)

    # Now try blocking each of the visited tiles from part one
    # and check if it causes a loop within the map
    loops = 0
    for i, tile in enumerate(visited, start=1):
        # Preserve the original traveled map
        m = deepcopy(original)
        m[tile[0]][tile[1]] = "#"
        loop = navigate_map(m, start, 'U')
        if loop:
            loops += 1
    print(loops)


if __name__ == '__main__':
    part_one()
    part_two()
