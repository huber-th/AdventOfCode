""" Advent of Code 2024 """
from pathlib import Path


def load_data(file: str):
    """
    Load and sanitize data

    Return: The loaded and sanitized file content for processing
    """
    p = Path(__file__).with_name(file)
    with p.open('r', encoding='utf8') as f:
        c = f.read().strip()
    return c


def part_one():
    """ Solution Implementation for Part 1 """
    data = load_data('test')
    print(data)

    print('Part one:')


def part_two():
    """ Solution Implementation for Part 2 """
    data = load_data('test')
    print(data)

    print('Part two:')


if __name__ == '__main__':
    part_one()
    part_two()
