""" filesystem paths module """
from pathlib import Path
import sys
sys.setrecursionlimit(4000)

def load_data(file: str):
    """ Load and sanitize data """
    p = Path(__file__).with_name(file)
    with p.open('r', encoding='utf8') as f:
        d = f.read().strip().split('\n')
        data = []
        for r in d:
            row = []
            for c in r:
                row.append(c)
            data.append(row)

    return data


def next_tile_coordinates(y, x, directions):
    """ Return the coordinates of the next tile """
    # print(f'{y} {x} and {directions} ({len(directions)})')
    coordinates = []
    for direction in directions:
        if direction == 'R':
            coordinates.append((y, x+1, 'R'))
        if direction == 'D':
            coordinates.append((y+1, x, 'D'))
        if direction == 'L':
            coordinates.append((y, x-1, 'L'))
        if direction == 'U':
            coordinates.append((y-1, x, 'U'))
    return tuple(coordinates)


def next_tiles(current, y, x, direction):
    """ Return the next tile and direction give the current tile and direction """
    next_dir = (direction)
    if current == '/':
        if direction == 'R':
            next_dir = ('U')
        if direction == 'D':
            next_dir = ('L')
        if direction == 'L':
            next_dir = ('D')
        if direction == 'U':
            next_dir = ('R')
    if current == '\\':
        if direction == 'R':
            next_dir = ('D')
        if direction == 'D':
            next_dir = ('R')
        if direction == 'L':
            next_dir = ('U')
        if direction == 'U':
            next_dir = ('L')
    if current == '|':
        if direction == 'R':
            next_dir = ('U', 'D')
        if direction == 'D':
            next_dir = ('D')
        if direction == 'L':
            next_dir = ('U', 'D')
        if direction == 'U':
            next_dir = ('U')
    if current == '-':
        if direction == 'R':
            next_dir = ('R')
        if direction == 'D':
            next_dir = ('L', 'R')
        if direction == 'L':
            next_dir = ('L')
        if direction == 'U':
            next_dir = ('L', 'R')
    return next_tile_coordinates(y, x, next_dir)


def solve(m, direction, y, x, em, seen):
    """ Recursively energize tiles """
    # print(f'Solving for {y} {x} and {direction}')
    if (y,x) not in seen:
        seen[y,x] = []
    if direction in seen[y,x]:
        return
    seen[y,x].append(direction)

    em[y][x] = '#'
    current = m[y][x]
    nxt = next_tiles(current, y, x, direction)
    for n in nxt:
        if n[0] >= 0 and n[0] < len(m) and n[1] >= 0 and n[1] < len(m[0]):
            em[n[0]][n[1]] = '#'
            solve(m, n[2], n[0], n[1], em, seen)


def empty_energized_matrix(matrix):
    """ Create empty matrix to mark energized tiles """
    em = []
    for _ in range(len(matrix)):
        emr = []
        for _ in range(len(matrix[0])):
            emr.append('.')
        em.append(emr)
    return em


def get_energized_tiles_after_n_moves(m, em):
    """ Count energized tiles """
    solve(m, 'R', 0, 0, em, {})


def get_energized_tile_count(em):
    """ Count energized tiles """
    res = 0
    for r in em:
        for s in r:
            if s == '#':
                res += 1
    return res


def get_max_energized_after_n_starting_outside(m):
    """ Get max energized starting anywhere outside """
    max_energized = 0
    # Move along left
    for i in range(0, len(m)):
        em = empty_energized_matrix(m)
        solve(m, 'R', i, 0, em, {})
        energized = get_energized_tile_count(em)
        if energized > max_energized:
            max_energized = energized
    # Move along top
    for i in range(0, len(m[0])):
        em = empty_energized_matrix(m)
        solve(m, 'D', 0, i, em, {})
        energized = get_energized_tile_count(em)
        if energized > max_energized:
            max_energized = energized
    # Move along bottom
    for i in range(0, len(m[0])):
        em = empty_energized_matrix(m)
        solve(m, 'U', len(m)-1, i, em, {})
        energized = get_energized_tile_count(em)
        if energized > max_energized:
            max_energized = energized
    # Move along right
    for i in range(0, len(m)):
        em = empty_energized_matrix(m)
        solve(m, 'L', i, len(m[0])-1, em, {})
        energized = get_energized_tile_count(em)
        if energized > max_energized:
            max_energized = energized
    return max_energized


if __name__ == '__main__':
    matrix = load_data('input')
    print('Part one:')
    em = empty_energized_matrix(matrix)
    get_energized_tiles_after_n_moves(matrix, em)
    res = 0
    for r in em:
        for s in r:
            if s == '#':
                res += 1
    print(res)
    print('Part two:')

    print(get_max_energized_after_n_starting_outside(matrix))
