""" Advent of Code 2024 """
from pathlib import Path


def load_data(file: str):
    """
    Load and sanitize data

    Return: The loaded and sanitized file content for processing
    """
    p = Path(__file__).with_name(file)
    with p.open('r', encoding='utf8') as f:
        c = [list(row) for row in f.read().strip().split('\n')]
    return c


def process_next(curr, dir, remaining, data):
    next = [curr[0] + dir[0], curr[1] + dir[1]]

    # Stop if we are outside the grid
    if (next[0] < 0 or
            next[1] < 0
            or next[1] >= len(data)
            or next[0] >= len(data[0])):
        return False

    # If next is not the next char in remaining stop
    if data[next[0]][next[1]] != remaining[0]:
        return False

    # If next is the last char we found what we are looking for
    if len(remaining) == 1:
        return True

    return process_next(next, dir, remaining[1:], data)


def find_xmas(data):
    count = 0
    directions = [
        [-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1]
    ]

    for y in range(len(data[0])):
        for x in range(len(data)):
            # Start checking in all directions for X
            if data[y][x] == 'X':
                for dir in directions:
                    if process_next([y, x], dir, "MAS", data):
                        count += 1
    return count


def part_one():
    """ Solution Implementation for Part 1 """
    data = load_data('input')

    print('Part one:')
    print(find_xmas(data))


def part_two():
    """ Solution Implementation for Part 2 """
    data = load_data('input')
    directions = [[[1, -1], [-1, 1]], [[-1, -1], [1, 1]]]

    print('Part two:')

    count = 0
    for y in range(len(data[0])):
        for x in range(len(data)):
            # Start checking from center or the X
            if data[y][x] == 'A':
                neighbours = []
                for dir in directions:
                    try:
                        next = [
                            [y + dir[0][0], x + dir[0][1]],
                            [y + dir[1][0], x + dir[1][1]]
                        ]
                        if any(num < 0 for sub_list in next
                               for num in sub_list):
                            continue
                        neighbours.append(
                            [data[next[0][0]][next[0][1]],
                             data[next[1][0]][next[1][1]]]
                        )
                    except IndexError:
                        continue
                # For X-MAS we need ech neighbour pair on both diagonals
                # to be M and S. Otherwise it does not complete X-MAS
                if (len(neighbours) > 0 and
                        all('M' in list and 'S' in list
                            for list in neighbours)):
                    count += 1
    print(count)


if __name__ == '__main__':
    part_one()
    part_two()
