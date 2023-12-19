""" filesystem paths module """
from pathlib import Path

def load_data(file: str):
    """ Load and sanitize data """
    p = Path(__file__).with_name(file)
    with p.open('r', encoding='utf8') as f:
        c = f.read().strip().split('\n')
    return c


def shoe_lace(points):
    """
    Calculate area between points using shoe lace
    https://en.wikipedia.org/wiki/Shoelace_formula
    """
    area: int = 0
    for i,_  in enumerate(points[1:], 1):
        a = points[i-1][0]
        b = points[i-1][1]
        c = points[i][0]
        d = points[i][1]
        sl = ((a * d) - (b * c))
        area += sl
    return area


def solve(dig_plan):
    directions = {'R': (1,0), 'D': (0,-1), 'L': (-1,0), 'U': (0,1)}
    # count points travelled to account for outline of blocks
    # meaning the outside points are 0.5 more than we record
    point_count = 0 
    position = [0,0]
    points = [position]
    # generate all points for shoe lace
    for dig in dig_plan:
        direction = directions[dig[0]]
        for _ in range(dig[1]):
            position = [sum(x) for x in zip(position, direction)] 
        point_count += dig[1]
        points.insert(0,position)
    # shoe lace + points travelled / 2 + 1 for the starting block
    print(shoe_lace(points)/2 + point_count/2 + 1)


if __name__ == '__main__':
    data = load_data('input')
    dig_plan = []
    for row in data:
        direction, steps, colour = row.split(' ')
        colour = colour.replace('(#','').replace(')','')
        dig_plan.append((direction, int(steps), colour))

    print('Part one:')
    solve(dig_plan)


    print('Part two:')
    converted_dig_plan = []
    for dig in dig_plan:
        steps_hex = dig[2][:5]
        d = dig[2][5:]
        steps = int(steps_hex, 16)
        if d == '0':
            dir = 'R'
        if d == '1':
            dir = 'D'
        if d == '2':
            dir = 'L'
        if d == '3':
            dir = 'U'
        converted_dig_plan.append([dir, steps])
    solve(converted_dig_plan)
