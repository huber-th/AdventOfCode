""" filesystem paths module """
from pathlib import Path


def load_data(file: str):
    """ Load and sanitize data """
    p = Path(__file__).with_name(file)
    with p.open('r', encoding='utf8') as f:
        c = f.read().strip().split('\n')
        columns = [''] * len(c[0])
        for row in c:
            for i, ch in enumerate(row):
                columns[i] += ch

    return columns


if __name__ == '__main__':
    data = load_data('input')

    print('Part one:')
    shifted = []
    for col in data:
        col = list(col)
        ncol = col
        to_move = []
        for i, ch in enumerate(reversed(col), 1):
            if ch == 'O':
                to_move.append(i)
            if (ch == '#' or i == len(ncol)) and len(to_move) > 0:
                if ch == '#':
                    idx = i-1
                else:
                    idx = i
                for m in reversed(to_move):
                    if idx == m:
                        idx -= 1
                        continue
                    ncol[-idx] = ncol[-m]
                    ncol[-m] = '.'
                    idx -= 1
                to_move = []
        shifted.append(ncol)

    load = 0
    for col in shifted:
        for i,ch in enumerate(reversed(col), 1):
            if ch == 'O':
                load += i

    print(load)

    print('Part two:')
