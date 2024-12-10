""" Advent of Code 2024 """
from pathlib import Path


def load_data():
    """
    Load and sanitize data

    Return: The loaded and sanitized file content for processing
    """
    p = Path(__file__).with_name('input')
    with p.open('r', encoding='utf8') as f:
        c = [list(map(int, row)) for row in f.read().strip().split('\n')]
    return c


def print_map(map):
    for row in map:
        print()
        for pos in row:
            print(pos, end='')
    print()
    print()


def navigate_trail(curr, map, ends, distinct):
    """
    Follow the trail as long as the level increases by 1 and determine
    how many level 9 spots we can reach
    """

    curr_level = map[curr[0]][curr[1]]

    if curr_level == 9:
        if not distinct:
            # mark trailhead as visited
            if curr not in ends:
                ends.append(curr)
                return 1
            else:
                # if we have already reached this end through a different path
                # don't count it again
                return 0
        else:
            return 1

    # directions R, D, L, U
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    res = 0
    for i in range(4):
        next = (curr[0] + directions[i][0], curr[1] + directions[i][1])

        if (next[0] < 0 or
                next[1] < 0 or
                next[0] >= len(map) or
                next[1] >= len(map[1])):
            continue

        next_level = map[next[0]][next[1]]

        if next_level == curr_level + 1:
            # print(f'{curr} at {curr_level} to {next} at {next_level}')
            # input()
            res += navigate_trail(next, map, ends, distinct)

    return res


def all():
    """ Solution Implementation for Part 1 """
    map = load_data()

    print('Part one:')
    trailheads = []
    for y, row in enumerate(map):
        for x, pos in enumerate(row):
            if pos == 0:
                trailheads.append((y, x))
    res = 0
    for trailhead in trailheads:
        score = navigate_trail(
            trailhead,
            map,
            [['.'] * len(map[0]) for _ in range(len(map))],
            False)
        res += score
    print(res)

    print('Part two:')

    res = 0
    for trailhead in trailheads:
        score = navigate_trail(
            trailhead,
            map,
            [['.'] * len(map[0]) for _ in range(len(map))], True)
        res += score
    print(res)


if __name__ == '__main__':
    all()
