""" Advent of Code 2024 """
from pathlib import Path
from collections import defaultdict


def load_data():
    """
    Load and sanitize data

    Return: The loaded and sanitized file content for processing
    """
    p = Path(__file__).with_name('input')
    with p.open('r', encoding='utf8') as f:
        c = [int(stone) for stone in f.read().strip().split(' ')]
    return c


def convert(stone):
    """
    Convert stones accordint to the rules:
    """
    # 1 if stone is 0
    if stone == 0:
        return [1]
    # Split digits in half if even length into two stones
    if len(str(stone)) % 2 == 0:
        s = str(stone)
        left = s[:len(s)//2]
        right = s[len(s)//2:]
        return [int(left), int(right)]
    # Multiply stone by 2024 otherwise
    else:
        return [2024 * stone]


def blink(stones):
    """
    Instead of growing the list of stones, we can use a dict {stone:count} to
    remember the count of a stone. This allows us to apply the rules and carry
    the count forward.

    e.g. if a stone 2024 has count 7, the convertion rules turn 2024 into two
    stones 20 and 24. Now since this happens to all 2024 stones, we can simply
    replace the entry in the dict with two entries for 20 and 24, both with
    value 7.

    This drastically reduces the size of the stone list as the iterations
    increases and at the same time reduces the amount of time we have to
    apply the conversion rules.
    """
    new_stones = defaultdict(int)
    for s in stones:
        s_count = stones[s]
        for r in convert(s):
            new_stones[r] += s_count
    return new_stones


def part_one():
    """ Solution Implementation for Part 1 """
    data = load_data()

    print('Part one:')
    stones = defaultdict(int)
    for s in data:
        stones[s] += 1

    for i in range(25):
        stones = blink(stones)

    res = 0
    for s in stones:
        res += stones[s]
    print(res)


def part_two():
    """ Solution Implementation for Part 2 """
    data = load_data()

    print('Part two:')
    stones = defaultdict(int)
    for s in data:
        stones[s] += 1

    for i in range(75):
        stones = blink(stones)

    res = 0
    for s in stones:
        res += stones[s]
    print(res)


if __name__ == '__main__':
    part_one()
    part_two()
