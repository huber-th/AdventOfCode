""" Advent of Code 2024 """
from pathlib import Path


def load_data():
    """
    Load and sanitize data

    Return: The loaded and sanitized file content for processing
    """
    p = Path(__file__).with_name('test')
    with p.open('r', encoding='utf8') as f:
        c = [list(map(int, rows.split('   ')))
             for rows in f.read().strip().split('\n')]
        s = [sorted(list) for list in list(zip(*c))]
    return s


def part_one():
    """
    Solution Implementation for Part 1

    Calculate the distance between each item in the two sorted lists
    """
    data = load_data()

    print('Part one:')

    distance = 0
    for i, val1 in enumerate(data[0]):
        distance += abs(val1 - data[1][i])
    print(distance)


def part_two():
    """
    Solution Implementation for Part 2

    For each item in list 1, count how often it occurs in list2.

    Then increase the simulation score
    by multiplying it's value with the count.
    """
    data = load_data()

    print('Part two:')

    sim_score = 0
    for val1 in data[0]:
        count = data[1].count(val1)
        sim_score += val1 * count
    print(sim_score)


if __name__ == '__main__':
    part_one()
    part_two()
