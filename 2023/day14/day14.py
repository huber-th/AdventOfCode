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

        ncol = []
        for row in columns:
            row = list(row)
            ncol.append(row)

    return ncol

def rotate_90_degree_clckwise(matrix):
    new_matrix = []
    for i in range(len(matrix[0])):
        li = list(map(lambda x: x[i], matrix))
        li.reverse()
        new_matrix.append(li)

    return new_matrix


def rotate_90_degree_anticlckwise(matrix):
    new_matrix = []
    for i in range(len(matrix[0]), 0, -1):
        new_matrix.append(list(map(lambda x: x[i-1], matrix)))

    return new_matrix


def print_matrix(matrix):
    print('------')
    for i in range(0,len(matrix[0])):
        row = ''
        for j in range(0,len(matrix)):
            row += matrix[j][i]
        print(row)
    print('------')


def shift_rocks(matrix):
    shifted = []
    for col in matrix:
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
    return shifted


def rotate_cycle(matrix):
    for _ in range(0,4):
        matrix = shift_rocks(matrix)
        matrix = rotate_90_degree_anticlckwise(matrix)
    return matrix


def calc_load(matrix):
    load = 0
    for col in matrix:
         for i,ch in enumerate(reversed(col), 1):
             if ch == 'O':
                 load += i
    return load


if __name__ == '__main__':
    data = load_data('input')
    print('Part one:')
    print(calc_load(shift_rocks(data)))

    print('Part two:')
    data = load_data('input')
    # Assumption that there is a loop at some point.
    # No need to run for 1,000,000,000 cycles
    n = 1000
    for i in range(0,n):
        data = rotate_cycle(data)
    print(calc_load(data))
