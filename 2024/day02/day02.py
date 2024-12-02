""" Advent of Code 2024 """
from pathlib import Path
from itertools import combinations


def load_data():
    """
    Load and sanitize data

    Return: The loaded and sanitized file content for processing
    """
    p = Path(__file__).with_name('input')
    with p.open('r', encoding='utf8') as f:
        c = [list(map(int, row.split(' ')))
             for row in f.read().strip().split('\n')]
    return c


def part_one():
    """ Solution Implementation for Part 1 """
    data = load_data()

    print('Part one:')
    safe_reports = 0
    for report in data:
        # Check for strictly increasing list
        increasing = all(i < j for i, j in zip(report, report[1:]))
        # Check for strictly decreasing list
        decreasing = all(i > j for i, j in zip(report, report[1:]))
        # Check for distance between pairs to be between 1 and at most 3
        distance_safe = all(abs(j-i) <= 3 and abs(j-i) >= 1
                            for i, j in zip(report, report[1:]))

        # Report is safe if strictly increasing or decreasing and the distance
        # of any level change is between 1 and 3
        if (increasing or decreasing) and distance_safe:
            safe_reports += 1
    print(safe_reports)


def part_two():
    """ Solution Implementation for Part 2 """
    data = load_data()

    print('Part two:')
    safe_reports = 0
    for report in data:
        # Generate all reports possible with one item missing and validate
        to_check = [list(combos) for combos
                    in combinations(report, len(report) - 1)]
        for combo in to_check:
            # Check for strictly increasing list
            increasing = all(i < j for i, j in zip(combo, combo[1:]))
            # Check for strictly decreasing list
            decreasing = all(i > j for i, j in zip(combo, combo[1:]))
            # Check for distance between pairs to be between 1 and at most 3
            distance_safe = all(abs(j-i) <= 3 and abs(j-i) >= 1
                                for i, j in zip(combo, combo[1:]))

            # combo is safe if strictly increasing or decreasing and
            # the distance of any level change is between 1 and 3
            if (increasing or decreasing) and distance_safe:
                safe_reports += 1
                break
    print(safe_reports)


if __name__ == '__main__':
    part_one()
    part_two()
