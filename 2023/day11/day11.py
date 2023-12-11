""" filesystem paths module """
from pathlib import Path
import itertools


def load_data(file: str) -> [str]:
    """ Load and sanitize data """
    p = Path(__file__).with_name(file)
    with p.open('r', encoding='utf8') as f:
        c = f.read().strip().split('\n')
    return c


def calculate_distance_between_galaxies(galaxy, expansion_multiplier):
    """ 
    Calculate the distance between all galaxy combinations 
    expansion_multiplier defines how often a column/row without
    a galaxy should be duplicated.
    """
    row_without_galaxy = []
    for i, row in enumerate(galaxy):
        if '#' not in row:
            row_without_galaxy.append(i)
    index_with_galaxy = []
    for i in range(0, len(galaxy[0])):
        for r in galaxy:
            if r[i] == '#':
                index_with_galaxy.append(i)
                break
    col_without_galaxy = []
    for i in range(0, len(galaxy[0])):
        if i not in index_with_galaxy:
            col_without_galaxy.append(i)
    galaxy_map = []
    for i, r in enumerate(galaxy):
        for j, c in enumerate(r):
            if c == '#':
                galaxy_map.append(f'{i}-{j}')
    combinations = list(itertools.combinations(galaxy_map, 2))

    distance_sum: int = 0

    for c in combinations:
        first = c[0].split('-')
        second = c[1].split('-')

        rows_crossed = []
        for i in range(int(first[0])+1, int(second[0])):
            rows_crossed.append(i)

        cols_crossed = []
        if (int(first[1])) <= int(second[1]):
            f = int(first[1])
            s = int(second[1])
        else:
            s = int(first[1])
            f = int(second[1])
        for i in range(f+1, s):
            cols_crossed.append(i)

        rows_multiplier = [v for v in rows_crossed if v in row_without_galaxy]
        cols_multiplier = [v for v in cols_crossed if v in col_without_galaxy]

        distance = abs((int(first[0]) - int(second[0]))) + \
            abs((int(first[1]) - int(second[1])))

        expansion = (len(rows_multiplier) * expansion_multiplier) + \
            (len(cols_multiplier) * expansion_multiplier)

        distance_sum += distance + expansion
    print(distance_sum)


if __name__ == '__main__':
    data = load_data('input')

    print('Part one:')
    print(calculate_distance_between_galaxies(data, 1))

    print('Part two:')
    print(calculate_distance_between_galaxies(data, 999999))
