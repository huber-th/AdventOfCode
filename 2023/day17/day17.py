""" filesystem paths module """
from pathlib import Path
from heapq import heappop, heappush


def load_data(file: str):
    """ Load and sanitize data """
    p = Path(__file__).with_name(file)
    with p.open('r', encoding='utf8') as f:
        d = f.read().strip().split('\n')
        data = []
        for r in d:
            row = []
            for c in r:
                row.append(int(c))
            data.append(row)
    return data


def calc_heat_heat_loss(matrix, min_steps, max_steps):
    """ Calculate heat heat_loss to get to bottom right with Djikstra """
    # directions lookup 0=LEFT, 1=UP, 2=DOWN, 3=RIGHT
    dir_x = [-1,0,0,1]
    dir_y = [0,-1,1,0]

    # heat_loss, x, y, steps, x-direction, y-direction)
    to_process = [(0, 0, 0, 0, 0, 0)] 
    processed = set()
    while to_process:
        heat_loss, x, y, k, dx, dy = heappop(to_process)

        if x == len(matrix) - 1 and y == len(matrix[0])-1:
            if k < min_steps:
                continue
            break

        if (x, y, k, dx, dy) in processed:
            continue

        processed.add((x, y, k, dx, dy))

        for i in range(4):
            new_dx = dir_x[i]
            new_dy = dir_y[i]

            if not new_dx == dx and not new_dy == dy and k < min_steps:
                continue

            if new_dx == dx and new_dy == dy:
                new_k = k + 1
            else:
                new_k = 1

            # Don't allow going into the same direction more than 3 times
            if new_k > max_steps:
                continue

            new_x, new_y = x + new_dx, y + new_dy

            # Don't go backwards where we came from
            if new_dx == -dx and new_dy == -dy:
                continue

            # New spot outside grid
            if new_x < 0 or new_y < 0 or new_x == len(matrix) or new_y == len(matrix[0]):
                continue

            new_heat_loss = heat_loss + matrix[new_x][new_y]

            heappush(to_process, (new_heat_loss, new_x, new_y, new_k, new_dx, new_dy))

    return heat_loss


if __name__ == '__main__':
    matrix = load_data('input')

    print('Part one:')
    print(calc_heat_heat_loss(matrix, 0, 3))

    print('Part two:')
    print(calc_heat_heat_loss(matrix, 4, 10))
