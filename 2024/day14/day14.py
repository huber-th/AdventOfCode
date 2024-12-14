""" Advent of Code 2024 """
from pathlib import Path
import re


def load_data():
    """
    Load and sanitize data

    Return: The loaded and sanitized file content for processing
    """
    p = Path(__file__).with_name('input')
    with p.open('r', encoding='utf8') as f:
        c = f.read().strip().split('\n')
        robots = []
        for r in c:
            p = re.findall(r'p\=(\d+),(\d+)', r)
            v = re.findall(r'v\=(-?\d+),(-?\d+)', r)
            robots.append((tuple(map(int, p[0])), tuple(map(int, v[0]))))
    return robots


def move_robots(robots, cols, rows):
    """ Move robots each one step """
    new_robots = []
    for r in robots:
        rx, ry = r[0]
        vx, vy = r[1]

        rx = (rx + vx) % cols
        ry = (ry + vy) % rows
        new_robots.append(((rx, ry), r[1]))

    return new_robots


def part_one():
    """ Solution Implementation for Part 1 """
    data = load_data()

    print('Part one:')
    rows = 103
    cols = 101

    for i in range(100):
        data = move_robots(data, cols, rows)

    cx = ((cols + 1) // 2) - 1
    cy = ((rows + 1) // 2) - 1
    q1 = 0
    q2 = 0
    q3 = 0
    q4 = 0
    for r in data:
        rx, ry = r[0]

        if rx < cx and ry < cy:
            q1 += 1
        if rx > cx and ry < cy:
            q2 += 1
        if rx > cx and ry > cy:
            q3 += 1
        if rx < cx and ry > cy:
            q4 += 1

    print(q1*q2*q3*q4)


def part_two():
    """ Solution Implementation for Part 2 """
    data = load_data()

    print('Part two:')

    rows = 103
    cols = 101

    i = 0
    while True:
        data = move_robots(data, cols, rows)
        coords = set()
        unique = True
        for r in data:
            if r[0] in coords:
                unique = False
                break
            else:
                coords.add(r[0])
        if unique:
            print(i + 1)
            break
        i += 1


if __name__ == '__main__':
    part_one()
    part_two()
