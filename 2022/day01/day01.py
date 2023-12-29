""" filesystem paths module """
from pathlib import Path


def load_data(file: str):
    """ Load and sanitize data """
    p = Path(__file__).with_name(file)
    with p.open('r', encoding='utf8') as f:
        return [
            [int(v) for v in x] for x in
            [l.split('\n') for l in f.read().strip().split('\n\n')]
        ]


if __name__ == '__main__':
    data = load_data('input')

    print('Part one:')
    print(max([sum([x for x in elf]) for elf in data]))

    print('Part two:')
    print(sum(sorted([sum([x for x in elf]) for elf in data])[-3:]))
