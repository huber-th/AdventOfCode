""" filesystem paths module """
from pathlib import Path

def load_data(file: str):
    """ Load and sanitize data """
    p = Path(__file__).with_name(file)
    with p.open('r', encoding='utf8') as f:
        rows = f.read().strip().split('\n')
        blocks = []
        for row in rows:
            blocks.append([
                [int(x) for x in rowsplit.split(',')]
                for rowsplit in row.split('~')
            ])
        return blocks


def solve1():
    highest, crucial = {}, {}
    for i, cube in enumerate(cubes):
        # determine xy base for the current cube
        base = [
            (x, y)
            for x in range(cube[0][0], cube[1][0] + 1)
            for y in range(cube[0][1], cube[1][1] + 1)
        ]

        best = [0, set()]
        for xy in base:
            if xy not in highest:
                continue
            height, cube_id = highest[xy]
            if height > best[0]:
                best = [height, set([cube_id])]
            elif height == best[0]:
                best[1].add(cube_id)

        if len(best[1]) == 1:
            crucial[best[1].pop()] = 1
        new_height = best[0] + cube[1][2] - cube[0][2] + 1
        for xy in base:
            highest[xy] = (new_height, i)
    return len(cubes) - len(crucial)


def solve2(remove_cube_id = None):
    highest, heights = {}, {}
    for i, cube in enumerate(cubes):
        if remove_cube_id == i:
            continue
        # determine xy base for the current cube
        base = [
            (x, y)
            for x in range(cube[0][0], cube[1][0] + 1)
            for y in range(cube[0][1], cube[1][1] + 1)
        ]

        best = [0, set()]
        for xy in base:
            if xy not in highest:
                continue
            height, cube_id = highest[xy]
            if height > best[0]:
                best = [height, set([cube_id])]
            elif height == best[0]:
                best[1].add(cube_id)

        heights[i] = best[0]
        new_height = best[0] + cube[1][2] - cube[0][2] + 1
        for xy in base:
            highest[xy] = (new_height, i)
    return heights

if __name__ == '__main__':
    data = load_data('input')

    # sort cube definitions
    cubes = sorted(data, key=lambda x: x[0][2])

    print('Part one:')
    print(solve1())
    print('Part two:')
    heights = solve2()
    res = 0
    for id, cube in enumerate(cubes):
        heights_without_cube = solve2(id)
        heights_without_cube[id] = -1
        res += sum(1 for c in range(len(cubes)) if heights_without_cube[c] != heights[c])
    print(res-len(cubes))

