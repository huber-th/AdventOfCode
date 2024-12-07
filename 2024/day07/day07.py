""" Advent of Code 2024 """
from pathlib import Path
from itertools import product


def load_data():
    """
    Load and sanitize data

    Return: The loaded and sanitized file content for processing
    """
    p = Path(__file__).with_name('input')
    with p.open('r', encoding='utf8') as f:
        c = [list([int(a), [int(v) for v in b.split(' ')]]) for a, b in [list(line.split(': ')) for line in f.read().strip().split('\n')]]
    return c


def part_one():
    """ Solution Implementation for Part 1 """
    data = load_data()

    print('Part one:')
    possible = []
    for d in data:
        combos = [''.join(combo) for combo in product(['+', '*'], repeat=len(d[1]) - 1)]
        for combo in combos:
            res = d[1][0]
            for i, value in enumerate(d[1][1:], start=1):
                c = combo[i - 1]
                if c == '+':
                    res += value
                elif c == '*':
                    res *= value
            if res == d[0]:
                if d not in possible:
                    possible.append(d)

    res = 0
    for p in possible:
        res += p[0]
    print(res)


def part_two():
    """ Solution Implementation for Part 2 """
    data = load_data()

    print('Part two:')
    possible = []
    for d in data:
        combos = [''.join(combo) for combo in product(['+', '*', '|'], repeat=len(d[1]) - 1)]
        for combo in combos:
            res = d[1][0]
            for i, value in enumerate(d[1][1:], start=1):
                c = combo[i - 1]
                if c == '|':
                    res = int(str(res) + str(value))
                if c == '+':
                    res += value
                elif c == '*':
                    res *= value
            if res == d[0]:
                if d not in possible:
                    possible.append(d)

    res = 0
    for p in possible:
        res += p[0]
    print(res)


if __name__ == '__main__':
    part_one()
    part_two()
