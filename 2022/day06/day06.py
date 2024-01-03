from pathlib import Path


def load_data(file: str):
    """ Load and sanitize data """
    p = Path(__file__).with_name(file)
    with p.open('r', encoding='utf8') as f:
        c = f.read().strip()
    return c


def find_marker(data: str, length: int) -> int:
    """
    Find the marker identifierd by a length of unique {length} characters
    """
    for i in range(length - 1, len(data)):
        if len(set(data[i-length:i])) == length:
            return i
    return - 1


if __name__ == '__main__':
    data = load_data('input')

    print('Part one:')
    print(find_marker(data, 4))

    print('Part two:')
    print(find_marker(data, 14))
