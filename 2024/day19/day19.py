""" Advent of Code 2024 """
from pathlib import Path
from functools import cache


def load_data():
    """
    Load and sanitize data

    Return: The loaded and sanitized file content for processing
    """
    p = Path(__file__).with_name('input')
    with p.open('r', encoding='utf8') as f:
        p, c = f.read().strip().split('\n\n')
        c = c.split('\n')
        p = tuple(p.split(', '))
    return p, c


@cache
def can_be_built(word, patterns):
    if len(word) == 0:
        return 1
    count = 0
    for i in range(len(word) + 1):
        c = word[0:i]
        if c in patterns:
            remaining = word[i:len(word)]
            count += can_be_built(remaining, patterns)
    return count


def all():
    """ Solution Implementation for Part 1 & 2"""
    patterns, towels = load_data()

    print('Part one:')
    count = 0
    combos = 0
    for towel in towels:
        cbb = can_be_built(towel, patterns)
        if cbb:
            count += 1
            combos += cbb
    print(count)

    print('Part two:')
    print(combos)


if __name__ == '__main__':
    all()
