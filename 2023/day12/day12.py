""" filesystem paths module """
from pathlib import Path
from functools import lru_cache


def load_data(file: str):
    """ Load and sanitize data """
    p = Path(__file__).with_name(file)
    with p.open('r', encoding='utf8') as f:
        c = f.read().strip().split('\n')
    return c


@lru_cache(maxsize=None, typed=False)
def solve(p, r, c):
    """ Solve the pattern one spot at a time """
    if len(c) == 0:
        if p.count('#') == 0:
            return 1
        else:
            return 0

    if len(p) == 0 and len(c) == 1 and r == c[0]:
        return 1

    if len(p) == 0 and len(c) > 0:
        return 0

    # Current spot is a ?
    if p[0] == '?':
        if not r:
            return solve('#'+p[1:], None, c) + solve('.'+p[1:], None, c)
        else:
            if r == c[0]:
                return solve(p[1:], None, c[1:])
            else:
                return solve(p[1:], r+1, c)

    # Current spot is a .
    if p[0] == '.':
        if not r:
            return solve(p[1:], None, c)
        else:
            if r == c[0]:
                return solve(p[1:], None, c[1:])
            else:
                return 0

    # Current spot is a #
    if p[0] == '#':
        if r:
            if r+1 == c[0] and len(p) > 1 and p[1] == '#':
                return 0
            if r == c[0]:
                return 0
            else:
                return solve(p[1:], r+1, c)
        else:
            return solve(p[1:], 1, c)
    return 0


if __name__ == '__main__':
    data = load_data('input')

    result: int = 0
    for row in data:
        split = row.split(' ')
        springs = split[0]
        counts = tuple(map(int, split[1].split(',')))
        result += solve(springs, None, counts)

    print('Part one:')
    print(result)

    print('Part two:')
    result: int = 0
    for row in data:
        split = row.split(' ')
        springs = split[0]
        counts = tuple(map(int, split[1].split(',')))
        nsprings = springs
        for _ in range(0, 4):
            nsprings += '?'
            nsprings += springs
        result += solve(nsprings, None, counts*5)
    print(result)
