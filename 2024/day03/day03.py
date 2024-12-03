""" Advent of Code 2024 """
from pathlib import Path
import re


def load_data(file: str):
    """
    Load and sanitize data

    Return: The loaded and sanitized file content for processing
    """
    p = Path(__file__).with_name(file)
    with p.open('r', encoding='utf8') as f:
        c = f.read().strip()
    return c


def find_regex(data: str):
    """ Find the keywords we are looking for by regex """
    pattern = r"mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\)"
    return re.findall(pattern, data)


def part_one():
    """ Solution Implementation for Part 1 """
    data = load_data('test')

    print('Part one:')
    res = 0
    instructions = find_regex(data)
    for entry in instructions:
        l, r = entry[4:-1].split(',')
        res += int(l) * int(r)
    print(res)


def part_two():
    """ Solution Implementation for Part 2 """
    data = load_data('input')

    print('Part two:')
    instructions = find_regex(data)
    do = True
    res = 0
    for entry in instructions:
        if entry == 'do()':
            do = True
        if entry == 'don\'t()':
            do = False
        if entry.startswith('mul'):
            l, r = entry[4:-1].split(',')
            if do:
                res += int(l) * int(r)
    print(res)


if __name__ == '__main__':
    part_one()
    part_two()
