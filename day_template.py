from pathlib import Path


def load_data(file: str):
    """ Load and sanitize data """
    p = Path(__file__).with_name(file)
    with p.open('r', encoding='utf8') as f:
        c = f.read().strip()
    print(c)
    return c


if __name__ == '__main__':
    data = load_data('test')

    print('Part one:')

    print('Part two:')
