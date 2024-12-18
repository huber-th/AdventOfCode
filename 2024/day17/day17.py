""" Advent of Code 2024 """
from pathlib import Path


def load_data():
    """
    Load and sanitize data

    Return: The loaded and sanitized file content for processing
    """
    p = Path(__file__).with_name('input')
    with p.open('r', encoding='utf8') as f:
        r, p = f.read().strip().split('\n\n')
        r = [int(row.split(' ')[2]) for row in r.split('\n')]
        p = [int(num) for num in p.split(' ')[1].split(',')]
    return r, p


def get_combo_op(op: int, a, b, c) -> int:
    """
    Get the combo op from the op

    Combo operands 0 through 3 represent literal values 0 through 3.
    Combo operand 4 represents the value of register A.
    Combo operand 5 represents the value of register B.
    Combo operand 6 represents the value of register C.
    Combo operand 7 is reserved and will not appear in valid programs.
    """

    if op == 4:
        return a
    elif op == 5:
        return b
    elif op == 6:
        return c
    else:
        return op


def run_program(p, a):
    """
    Execute the instruction provided according to the rules
    """

    b, c = 0, 0
    pointer = 0
    out = ''

    while pointer < len(p):
        code = p[pointer]
        op = p[pointer + 1]

        if code == 0:
            a //= 2 ** get_combo_op(op, a, b, c)
        elif code == 1:
            b ^= op
        elif code == 2:
            b = get_combo_op(op, a, b, c) % 8
        elif code == 3:
            if a != 0:
                pointer = op
                continue
        elif code == 4:
            b ^= c
        elif code == 5:
            out += str(get_combo_op(op, a, b, c) % 8) + ','
        elif code == 6:
            b = a // (2 ** get_combo_op(op, a, b, c))
        elif code == 7:
            c = a // (2 ** get_combo_op(op, a, b, c))
        pointer += 2
    return out[:-1]


def part_one():
    """ Solution Implementation for Part 1 """
    r, p = load_data()

    print('Part one:')
    # Trim the last ,
    print(run_program(p, r[0])[:-1])


def part_two():
    """ Solution Implementation for Part 2 """
    _, p = load_data()

    print('Part two:')
    # Found by doing large steps until the last 4 digits matched, and then
    # reduced the step size for the next couple of digits
    i = 164278899142333
    while True:
        # print(f'Running for {i}')
        out = run_program(p, i)
        if out.endswith('2,4,1,1,7,5,1,5,4,3,5,5,0,3,3,0'):
            print(i)
            break
        i += 1


if __name__ == '__main__':
    part_one()
    part_two()
