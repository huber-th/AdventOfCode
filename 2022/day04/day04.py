from pathlib import Path


def load_data(file: str):
    """ Load and sanitize data """
    p = Path(__file__).with_name(file)
    with p.open('r', encoding='utf8') as f:
        return [pair.split(',') for pair in f.read().strip().split('\n')]


def contained(pair, full_only: bool) -> int:
    """
    Return 1 if one range is fully contained in the other
    """
    first, second = pair
    fs, fe = [int(x) for x in first.split('-')]
    ss, se = [int(x) for x in second.split('-')]
    frange = range(fs,fe+1)
    srange = range(ss,se+1)
    overlap = set(frange).intersection(srange)
    if full_only:
        return 1 if len(overlap) == len(frange) or len(overlap) == len(srange) else 0
    else:
        return 1 if len(overlap) > 0 else 0


if __name__ == '__main__':
    pairs = load_data('input')

    print('Part one:')
    result: int = 0
    for pair in pairs:
        result += contained(pair, True)
    print(result)

    print('Part two:')
    result: int = 0
    for pair in pairs:
        result += contained(pair, False)
    print(result)
