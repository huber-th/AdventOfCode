""" filesystem paths module """
from pathlib import Path


def load_data(file: str):
    """ Load and sanitize data """
    p = Path(__file__).with_name(file)
    with p.open('r', encoding='utf8') as f:
        c = f.read().strip().split('\n')
        data = []
        for r in c:
            row = []
            for s in r:
                row.append(s)
            data.append(row)
    return data


def print_matrix(matrix: list[list[str]]):
    for r in matrix:
        o = ''
        for c in r:
            o += c
        print(o)
    print('----------------')


def bfs(matrix: list[list[str]], queue: list[tuple[int, int, int]], max_depth: int):
    """ solve using breadth first search to mark the positions step by step """
    # right, down, left, up
    dx = [1,0,-1,0]
    dy = [0,1,0,-1]

    visited = []

    while len(queue) > 0:
        current = queue.pop(0)
        if (current[0],current[1]) in visited:
            continue
        visited.append((current[0],current[1]))
        for i in range(4):
            x = current[0] + dx[i]
            y = current[1] + dy[i]

            # if next is outside of grid, skip
            if x < 0 or x >= len(matrix[0]) or y < 0 or y >= len(matrix[0]):
                continue

            # if next is a wall, skip
            if matrix[y][x] == '#':
                continue

            # if steps are odd we can't reach it in an even number of steps
            matrix[y][x] = 'O' if (current[2]+1) % 2 == 0 else '.'
            if current[2]+1 < max_depth:
                queue.append((x,y, current[2]+1))


if __name__ == '__main__':
    data = load_data('input')
    x = -1
    y = -1
    for i, d in enumerate(data):
        for j, c in enumerate(d):
            if c == 'S':
                x = j
                y = i
    data[y][x] = 'O'

    print('Part one:')
    bfs(data, [(x, y, 0)], 64)
    res: int = 0
    for r in data:
        for c in r:
            if c == 'O':
                res += 1
    print(res)
    print('Part two:')
