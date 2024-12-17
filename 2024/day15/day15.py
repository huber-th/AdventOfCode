""" Advent of Code 2024 """
from pathlib import Path


def load_data():
    """
    Load and sanitize data

    Return: The loaded and sanitized file content for processing
    """
    p = Path(__file__).with_name('input')
    with p.open('r', encoding='utf8') as f:
        map, moves = f.read().strip().split('\n\n')
        map = [list(row) for row in map.split('\n')]
        moves = moves.replace('\n', '')
    return [map, moves]


def draw_map(map):
    for row in map:
        print()
        for tile in row:
            print(tile, end='')
    print()


def move_robot(map, move, robot):

    # Start with defaut right
    dy, dx = (0, 1)

    if move == 'v':
        # Down
        dy, dx = (1, 0)
    elif move == '<':
        # Left
        dy, dx = (0, -1)
    elif move == '^':
        # Up
        dy, dx = (-1, 0)

    curr_row = [(robot[0], robot[1])]
    to_shift = [curr_row]
    while True:
        nxt_row = []
        for curr_y, curr_x in curr_row:
            if map[curr_y][curr_x] == '.':
                # If current row tile is '.' we don't have to continue
                # with this tile
                continue
            nxt_y = curr_y + dy
            nxt_x = curr_x + dx
            if move == '<' or move == '>':
                nxt_row.append((nxt_y, nxt_x))
            else:
                if map[nxt_y][nxt_x] == '[':
                    if (nxt_y, nxt_x) not in nxt_row:
                        nxt_row.append((nxt_y, nxt_x))
                    if (nxt_y, nxt_x + 1) not in nxt_row:
                        nxt_row.append((nxt_y, nxt_x + 1))
                elif map[nxt_y][nxt_x] == ']':
                    if (nxt_y, nxt_x) not in nxt_row:
                        nxt_row.append((nxt_y, nxt_x))
                    if (nxt_y, nxt_x - 1) not in nxt_row:
                        nxt_row.append((nxt_y, nxt_x - 1))
                else:
                    nxt_row.append((nxt_y, nxt_x))

        hit_wall = False
        for nxt_y, nxt_x in nxt_row:
            if map[nxt_y][nxt_x] == '#':
                # If there is a wall in front of any of the current row before
                # we find an all free row, we can't move
                to_shift = set()
                hit_wall = True

        if hit_wall:
            break

        to_shift.append(nxt_row)

        all_free = True
        for nxt_y, nxt_x in nxt_row:
            if map[nxt_y][nxt_x] != '.':
                all_free = False

        if all_free:
            break

        # Remove all '.' tiles as we don't have to continue to process
        # them as the previous tile can be moved without affect
        sanitized_nxt_row = []
        for ty, tx in to_shift[len(to_shift) - 1]:
            if map[ty][tx] != '.':
                sanitized_nxt_row.append((ty, tx))

        to_shift[len(to_shift) - 1] = sanitized_nxt_row
        curr_row = sanitized_nxt_row

    new_robot = robot
    # Last entry in to_shift is the empty spot, therefore start from
    # the second last item going backwards
    # print(to_shift)
    rows = list(to_shift)
    for i, row in enumerate(rows[-2::-1]):
        for tile in row:
            ty, tx = tile
            map[ty + dy][tx + dx] = map[ty][tx]
            # If the tile behind this isn't in the next row, set it to '.'
            # as it's indirectely pushed
            # - 2 since we start with the second last item
            idx = len(to_shift) - i - 2
            if idx >= 0 and (ty + dy, tx + dx) not in to_shift[idx]:
                map[ty][tx] = '.'
            new_robot = (ty + dy, tx + dx)

    return map, new_robot


def find_robot(map):
    for y, row in enumerate(map):
        for x, tile in enumerate(row):
            if tile == '@':
                return (y, x)
    return None


def part_one():
    """ Solution Implementation for Part 1 """
    map, moves = load_data()

    print('Part one:')
    # Find robots starting position
    robot = find_robot(map)

    for move in moves:
        map, robot = move_robot(map, move, robot)

    gps = 0
    for y, row in enumerate(map):
        for x, tile in enumerate(row):
            if tile == 'O':
                gps += y * 100 + x

    print(gps)


def convert_map(map):
    new_map = []
    for row in map:
        new_row = []
        for tile in row:
            if tile == '#':
                new_row.append('#')
                new_row.append('#')
            if tile == 'O':
                new_row.append('[')
                new_row.append(']')
            if tile == '.':
                new_row.append('.')
                new_row.append('.')
            if tile == '@':
                new_row.append('@')
                new_row.append('.')
        new_map.append(new_row)
    return new_map


def part_two():
    """ Solution Implementation for Part 2 """
    map, moves = load_data()
    map = convert_map(map)

    print('Part two:')
    robot = find_robot(map)

    i = 0
    for j, move in enumerate(moves):
        i += 1
        map, robot = move_robot(map, move, robot)

    gps = 0
    for y, row in enumerate(map):
        for x, tile in enumerate(row):
            if tile == '[':
                gps += y * 100 + x

    print(gps)


if __name__ == '__main__':
    part_one()
    part_two()
