from pathlib import Path


def load_data(file: str):
    """ Load and sanitize data """
    p = Path(__file__).with_name(file)
    with p.open('r', encoding='utf8') as f:
        c = [list(x) for x in f.read().strip().split('\n')]
    return c


def is_within_matrix(matrix: list[list[str]], cell: tuple[int, int]) -> int:
    return 0 <= cell[0] < len(matrix[0]) and 0 <= cell[1] < len(matrix)


def is_cell_visible(matrix: list[list[str]], cell: tuple[int, int]) -> int:

    directions = ((1, 0), (0, -1), (-1, 0), (0, 1))

    for direction in directions:
        pos = cell

        visible = True
        tree = matrix[pos[1]][pos[0]]
        # Check if all trees into the given direction are smaller
        pos = (pos[0] + direction[0], pos[1] + direction[1])
        while is_within_matrix(matrix, pos):
            curr = matrix[pos[1]][pos[0]]
            if curr >= tree:
                visible = False
                break
            pos = (pos[0] + direction[0], pos[1] + direction[1])
        if visible:
            return 1
    return 0


def determine_visibility(matrix: list[list[str]]) -> list[list[int]]:
    """
    Determine if a cell is visible from any direction. Return a matrix
    with bool values indicating if it is visible or not.

    A cell is visible if all cells into the direction are smaller
    """
    visibility = [[0 for _ in range(len(matrix[0]))]
                  for _ in range(len(matrix))]

    # all trees around the outside are always visible
    for i in range(len(matrix[0])):
        visibility[0][i] = 1
        visibility[len(matrix)-1][i] = 1

    for i in range(len(matrix)):
        visibility[i][0] = 1
        visibility[i][len(matrix[0])-1] = 1

    for i in range(1, len(matrix[0])-1):
        for j in range(1, len(matrix)-1):
            visibility[i][j] = is_cell_visible(matrix, (i, j))

    return visibility


def get_scenic_score(matrix: list[list[str]], cell: tuple[int, int]) -> int:

    directions = ((1, 0), (0, -1), (-1, 0), (0, 1))
    scores: list[int] = []
    for direction in directions:
        pos = cell
        score = 0

        tree = matrix[pos[1]][pos[0]]
        # Check if all trees into the given direction are smaller
        pos = (pos[0] + direction[0], pos[1] + direction[1])
        while is_within_matrix(matrix, pos):
            curr = matrix[pos[1]][pos[0]]
            score += 1
            if curr >= tree:
                break
            pos = (pos[0] + direction[0], pos[1] + direction[1])
        scores.append(score)
    scenic_score = 1
    for score in scores:
        scenic_score *= score
    return scenic_score


def determine_scenic_score(matrix: list[list[str]]) -> list[list[int]]:
    """
    Determine if a cell is visible from any direction. Return a matrix
    with bool values indicating if it is visible or not.

    A cell is visible if all cells into the direction are smaller
    """
    scenic_score = [[0 for _ in range(len(matrix[0]))]
                    for _ in range(len(matrix))]

    # all trees around the outside are always visible
    for i in range(len(matrix[0])):
        scenic_score[0][i] = 1
        scenic_score[len(matrix)-1][i] = 1

    for i in range(len(matrix)):
        scenic_score[i][0] = 1
        scenic_score[i][len(matrix[0])-1] = 1

    for i in range(1, len(matrix[0])-1):
        for j in range(1, len(matrix)-1):
            scenic_score[i][j] = get_scenic_score(matrix, (i, j))

    return scenic_score


if __name__ == '__main__':
    matrix = load_data('input')

    print('Part one:')
    res: int = 0
    for row in determine_visibility(matrix):
        for col in row:
            res += col
    print(res)

    print('Part two:')
    res: int = 0
    for row in determine_scenic_score(matrix):
        for col in row:
            res = col if col > res else res
    print(res)
