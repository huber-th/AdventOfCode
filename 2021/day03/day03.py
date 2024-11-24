""" Advent of Code """
from pathlib import Path


def load_data(file: str):
    """ Load and sanitize data """
    p = Path(__file__).with_name(file)
    with p.open('r', encoding='utf8') as f:
        c = [list(d) for d in f.read().strip().split('\n')]
        c = [[int(item) for item in row] for row in c]
    return c


def bit_to_int(val: str):
    """ Convert bit string to int """
    return int(val, 2)


def main():
    ''' Entry point '''
    data = load_data('test')

    print('Part one:')
    gamma = []
    epsilon = []
    for i in range(len(data[0])):
        values = [lst[i] for lst in data]
        total = sum(values)
        if total > len(values)/2:
            gamma.append(1)
            epsilon.append(0)
        else:
            gamma.append(0)
            epsilon.append(1)

    gamma = bit_to_int(''.join(map(str, gamma)))
    epsilon = bit_to_int(''.join(map(str, epsilon)))
    print(gamma * epsilon)

    print('Part two:')


if __name__ == '__main__':
    main()
