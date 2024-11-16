""" Advent of Code """
from pathlib import Path


def load_data(file: str):
    """ Load and sanitize data """
    p = Path(__file__).with_name(file)
    with p.open('r', encoding='utf8') as f:
        c = [int(x) for x in f.read().strip().split('\n')]
    return c


def main():
    ''' Entry point '''
    data = load_data('input')

    print('Part one:')
    print(sum(1 for prev, curr in zip(data, data[1:]) if curr > prev))

    print('Part two:')
    print(sum(1 for a, b, c, d in
              zip(data, data[1:], data[2:], data[3:]) if a+b+c < b+c+d))


if __name__ == '__main__':
    main()
