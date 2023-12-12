""" filesystem paths module """
from pathlib import Path


def load_data(file: str):
    """ Load and sanitize data """
    p = Path(__file__).with_name(file)
    with p.open('r', encoding='utf8') as f:
        c = f.read().strip().split('\n')
    return c


def validate_row(r) -> bool:
    """ Validate a row """
    split = r.split(' ')
    counts = list(map(int, split[1].split(',')))
    row_spring_counts = []
    counter = 0
    for c in split[0]:
        if c == '#':
            counter += 1
        elif counter > 0:
            row_spring_counts.append(counter)
            counter = 0
    if counter > 0:
        row_spring_counts.append(counter)
    return counts == row_spring_counts


def generate_combinations(n, combination, all_combinations):
    """ Generate combinations """
    if n == 0:
        all_combinations.append(''.join(combination))
        return

    combination[n - 1] = '.'
    generate_combinations(n - 1, combination, all_combinations)

    combination[n - 1] = '#'
    generate_combinations(n - 1, combination, all_combinations)


def generate_all_combinations(count_unknown):
    """ 
    Genreate all combinations of # and . for the amount 
    of unknown spots 
    """
    all_combinations = []
    initial_combination = [''] * count_unknown
    generate_combinations(count_unknown,
                          initial_combination, all_combinations)

    return all_combinations


def fill_question_marks(row, possible_combinations):
    """ Fill question marks """
    filled_rows = []
    for c in possible_combinations:
        combo = row
        for s in c:
            combo = combo.replace('?', s, 1)
        filled_rows.append(combo)
    return filled_rows


def find_valid_arrangements(row_with_unknowns) -> int:
    """ Find all possible arrangements to complete the row """
    # Count ? in row
    count_unknowns = row_with_unknowns.count('?')
    possible_combinations = generate_all_combinations(count_unknowns)
    row_combinations = fill_question_marks(
        row_with_unknowns, possible_combinations)
    valid_combinations = 0
    for r in row_combinations:
        if validate_row(r):
            valid_combinations += 1
    return valid_combinations


if __name__ == '__main__':
    data = load_data('input')

    print('Part one:')
    result: int = 0
    for row in data:
        result += find_valid_arrangements(row)
    print(result)

    print('Part two:')
