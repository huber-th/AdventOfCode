""" Advent of Code """
from pathlib import Path


def load_data(file: str):
    """ Load and sanitize data """
    p = Path(__file__).with_name(file)
    with p.open('r', encoding='utf8') as f:
        raw = [x.split(' ') for x in f.read().strip().split('\n')]
        moves = []
        for r in raw:
            moves.append((r[0], int(r[1])))
        return moves


def main():
    ''' Entry point '''
    data = load_data('input')

    horizontal = 0
    depth = 0
    depth2 = 0
    aim = 0
    for move in data:
        if move[0] == 'forward':
            horizontal += move[1]
            depth2 += aim * move[1]
        elif move[0] == 'down':
            depth += move[1]
            aim += move[1]
        elif move[0] == 'up':
            depth -= move[1]
            aim -= move[1]

    print('Part one:')
    print(f'Horizontal position: {horizontal}')
    print(f'Depth position: {depth}')
    print(f'Answer: {horizontal * depth}')

    print('Part two:')
    print(f'Horizontal position: {horizontal}')
    print(f'Depth position: {depth2}')
    print(f'Answer: {horizontal * depth2}')


if __name__ == '__main__':
    main()
