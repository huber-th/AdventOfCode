from pathlib import Path


def load_data(file: str):
    """ Load and sanitize data """
    p = Path(__file__).with_name(file)
    with p.open('r', encoding='utf8') as f:
        c = [r.split(' ') for r in f.read().strip().split('\n')]
    return c


def compute_cycles(d):
    """
    Calculate the values at the end of each cycle
    """
    values = {}

    nxt = 1
    val = 1
    for instruction in d:
        if instruction[0] == 'addx':
            values[nxt] = val
            nxt += 1
            val += int(instruction[1])
            values[nxt] = val
            nxt += 1
        if instruction[0] == 'noop':
            values[nxt] = val
            nxt += 1

    return values


def draw_pixel(crt, nxt, sprite):
    """
    Draw a single pixel on the crt
    """
    crt[nxt // 40][nxt % 40] = '#' if nxt % 40 in sprite else '.'
    return nxt + 1


def draw_crt(d):
    """
    Draw the CRT
    """
    crt = [[' '] * 40 for _ in range(6)]

    sprite = [-1, -1, -1]
    val = 1
    nxt = 0

    for instruction in d:
        sprite = [val - 1, val, val + 1]
        if instruction[0] == 'addx':
            nxt = draw_pixel(crt, nxt, sprite)
            nxt = draw_pixel(crt, nxt, sprite)
            val += int(instruction[1])
        if instruction[0] == 'noop':
            nxt = draw_pixel(crt, nxt, sprite)

    for row in crt:
        print(''.join(row))


if __name__ == '__main__':
    data = load_data('input')

    print('Part one:')
    cycles = compute_cycles(data)
    res: int = 0
    for cycle in (20, 60, 100, 140, 180, 220):
        # c - 1 since we need the value during and not after the cycle
        res += cycles[cycle-1] * cycle
    print(res)

    print('Part two:')
    draw_crt(data)
