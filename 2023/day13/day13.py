""" filesystem paths module """
from pathlib import Path


def load_data(file: str):
    """ Load and sanitize data """
    p = Path(__file__).with_name(file)
    with p.open('r', encoding='utf8') as f:
        c = f.read().strip().split('\n\n')
        patterns = []
        for pattern in c:
            rows = []
            for row in pattern.split('\n'):
                rows.append([*row])
            patterns.append(rows)
    return patterns


def rows_above_reflection(pattern):
    for i, row in enumerate(pattern, 1):
        if i >= len(pattern):
            return 0
        if pattern[i-1] == pattern[i]:
            idx = i-2
            gap = 3
            reflection = True
            while idx >= 0:
                if idx + gap > len(pattern) - 1:
                    break
                if pattern[idx] != pattern[idx + gap]:
                    reflection = False
                    break
                idx -= 1
                gap += 2
            if reflection:
                return i
    return 0


def is_horizontal_reflection(pattern, idx, gap):
    for r in pattern:
        if r[idx] != r[gap]:
            return False
    return True


def rows_left_of_reflection(pattern):
    for i in range(1, len(pattern[0])):
        if i > len(pattern[0]):
            return 0
        reflection = is_horizontal_reflection(pattern, i, i-1)
        if reflection:
            idx = i-2
            gap = 3
            while idx >= 0:
                if idx + gap > len(pattern[0]) - 1:
                    break
                if not is_horizontal_reflection(pattern, idx, idx + gap):
                    reflection = False
                    break
                idx -= 1
                gap += 2
            if reflection:
                return i
    return 0


if __name__ == '__main__':
    data = load_data('input')

    print('Part one:')
    result: int = 0
    for pattern in data:
        rlor: int = rows_left_of_reflection(pattern)
        if rlor == 0:
            rabv = rows_above_reflection(pattern)
            result += 100 * rabv
        else:
            result += rlor
    print(result)
    print('Part two:')
