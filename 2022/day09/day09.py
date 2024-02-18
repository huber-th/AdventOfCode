from pathlib import Path


def load_data(file: str):
    """ Load and sanitize data """
    p = Path(__file__).with_name(file)
    with p.open('r', encoding='utf8') as f:
        c = [(x[0], int(x[1])) for x in
             [r.split(' ') for r in f.read().strip().split('\n')]]
    return c


def make_tail_follow(h, t):
    """
    Ensure tail follows head according to the rules
    """
    hx, hy = h
    tx, ty = t

    # Up + Right
    if hy - ty > 1 and hx - tx > 1:
        ty += 1
        tx += 1
    # Down + Right
    if ty - hy > 1 and hx - tx > 1:
        ty -= 1
        tx += 1
    # Up + Left
    if hy - ty > 1 and tx - hx > 1:
        ty += 1
        tx -= 1
    # Down + Left
    if ty - hy > 1 and tx - hx > 1:
        ty -= 1
        tx -= 1
    # Up
    if hy - ty > 1:
        ty += 1
        tx = hx
    # Right
    if hx - tx > 1:
        tx += 1
        ty = hy
    # Down
    if ty - hy > 1:
        ty -= 1
        tx = hx
    # Left
    if tx - hx > 1:
        tx -= 1
        ty = hy
    return [tx, ty]


def print_rope(rope, tail_trail):
    """
    Print the rope and the trail of the tail
    """
    minx = miny = maxx = maxy = 0
    for knot in tail_trail:
        if knot[0] < minx:
            minx = knot[0]
        if knot[0] > maxx:
            maxx = knot[0]
        if knot[1] < miny:
            miny = knot[1]
        if knot[1] > maxy:
            maxy = knot[1]
    for knot in rope:
        if knot[0] < minx:
            minx = knot[0]
        if knot[0] > maxx:
            maxx = knot[0]
        if knot[1] < miny:
            miny = knot[1]
        if knot[1] > maxy:
            maxy = knot[1]

    matrix = []
    i = 0
    print(rope)
    for y in reversed(range(miny, maxy + 1)):
        matrix.append([])
        j = 0
        for x in range(minx, maxx + 1):
            matrix[i].append('O' if [x, y] in rope else ' ')
            j += 1
        i += 1
    i = 0
    for y in reversed(range(miny, maxy + 1)):
        j = 0
        for x in range(minx, maxx + 1):
            if (x, y) in tail_trail:
                matrix[i][j] = 'X'
            j += 1
        i += 1

    for row in matrix:
        print(row)


def walk_the_rope(s, k):
    """
    Walk the head the provided steps and track how the tail follows
    """
    rope = [[0, 0]]*k

    directions = {
        'U': (0, 1),
        'R': (1, 0),
        'D': (0, -1),
        'L': (-1, 0),
    }

    tail_trail = set()
    for step in s:
        for _ in range(step[1]):
            d = directions[step[0]]
            # print_rope(rope, tail_trail)
            rope[0] = [rope[0][0] + d[0], rope[0][1] + d[1]]
            for i in range(1, len(rope)):
                # print_rope(rope, tail_trail)
                # input('Wait ...')
                rope[i] = make_tail_follow(rope[i-1], rope[i])
                if i == len(rope) - 1:
                    tail_trail.add((rope[i][0], rope[i][1]))

    # print_rope(rope, tail_trail)
    return tail_trail


if __name__ == '__main__':
    steps = load_data('input')

    print('Part one:')
    print(len(walk_the_rope(steps, 2)))

    print('Part two:')
    print(len(walk_the_rope(steps, 10)))
