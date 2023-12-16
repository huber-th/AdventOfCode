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


def get_number_of_different_items(one, two):
    """ 
    Check how many elements are different between
    the two lines
    """
    return sum(1 for a, b in zip(one, two) if a != b)


def idx_vertical_reflection_line(p, i, j, with_smudge, smudge_used=False):
    """ Determine if the column i and j in p are reflections """
    if i < 0:
        if not with_smudge:
            return True
        else:
            if not smudge_used:
                return False
            else:
                return True
    if j > len(p[0])-1:
        if not with_smudge:
            return True
        else:
            if not smudge_used:
                return False
            else:
                return True

    col_i = [row[i] for row in p]
    col_j = [row[j] for row in p]
    if with_smudge:
        difference = get_number_of_different_items(col_i, col_j)
        if difference > 1:
            return False

        if difference == 1:
            if smudge_used:
                return False
            else:
                return idx_vertical_reflection_line(p, i-1, j+1, True, True)
        return idx_vertical_reflection_line(p, i-1, j+1, True, smudge_used)
    else:
        if col_i == col_j:
            return idx_vertical_reflection_line(p, i-1, j+1, False)
        else:
            return False
 

def idx_horizontal_reflection_line(p, i, j, with_smudge, smudge_used=False):
    """ Determine if the row i and j in p are reflections """
    if i < 0:
        if not with_smudge:
            return True
        else:
            if not smudge_used:
                return False
            else:
                return True
    if j > len(p)-1:
        if not with_smudge:
            return True
        else:
            if not smudge_used:
                return False
            else:
                return True


    if with_smudge:
        difference = get_number_of_different_items(p[i], p[j])
        if difference > 1:
            return False

        if difference == 1:
            if smudge_used:
                return False
            else:
                return idx_horizontal_reflection_line(p, i-1, j+1, True, True)
        return idx_horizontal_reflection_line(p, i-1, j+1, True, smudge_used)
    else:
        if p[i] == p[j]:
            return idx_horizontal_reflection_line(p, i-1, j+1, False)
        else:
            return False


if __name__ == '__main__':
    data = load_data('input')

    print('Part one:')
    result = 0
    for pattern in data:
        done = False
        for i in range(1, len(pattern)):
            if idx_horizontal_reflection_line(pattern, i-1, i, False):
                result += i * 100
                done = True
        if not done:
            for i in range(1, len(pattern[0])):
                if idx_vertical_reflection_line(pattern, i-1, i, False):
                    result += i

    print(result)
    print('Part two:')
    result = 0
    for pattern in data:
        done = False
        for i in range(1, len(pattern)):
            if idx_horizontal_reflection_line(pattern, i-1, i, True):
                result += i * 100
                done = True
        if not done:
            for i in range(1, len(pattern[0])):
                if idx_vertical_reflection_line(pattern, i-1, i, True):
                    result += i
    print(result)
