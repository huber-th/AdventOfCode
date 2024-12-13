""" Advent of Code 2024 """
from pathlib import Path
import re
from sympy import symbols, Eq, solve
from sympy.core.numbers import Integer


class Machine():
    """ Claw Machine representation """

    def __init__(self, definition, part2) -> None:
        parts = definition.split('\n')
        matches = re.findall(r'\+(\d+)', parts[0])
        self.ax, self.ay = [int(match) for match in matches]
        matches = re.findall(r'\+(\d+)', parts[1])
        self.bx, self.by = [int(match) for match in matches]
        matches = re.findall(r'\=(\d+)', parts[2])
        self.px, self.py = [int(match) for match in matches]
        if part2:
            self.px += 10000000000000
            self.py += 10000000000000

    def __str__(self):
        return f'ButtonA {self.ax}/{self.ay}, ' \
               f'ButtonB {self.bx}/{self.by} and ' \
               f'Prize {self.px}/{self.py}'


def load_data():
    """
    Load and sanitize data

    Return: The loaded and sanitized file content for processing
    """
    p = Path(__file__).with_name('input')
    with p.open('r', encoding='utf8') as f:
        c = f.read().strip().split('\n\n')
    return c


def solve_machines(machines):
    """
    Find the cost to solve the machines
    """
    cost = 0
    for m in machines:
        a, b = symbols('a b')
        eq1 = Eq(a * m.ax + b * m.bx, m.px)
        eq2 = Eq(a * m.ay + b * m.by, m.py)

        solution = solve((eq1, eq2), (a, b))
        if (isinstance(solution[a], Integer) and
                isinstance(solution[b], Integer)):
            cost += solution[a] * 3 + solution[b] * 1
    return cost


def part_one():
    """ Solution Implementation for Part 1 """
    data = load_data()
    machines = []
    for m in data:
        machines.append(Machine(m, False))

    print('Part one:')
    print(solve_machines(machines))


def part_two():
    """ Solution Implementation for Part 2 """
    data = load_data()
    machines = []
    for m in data:
        machines.append(Machine(m, True))

    print('Part two:')
    print(solve_machines(machines))


if __name__ == '__main__':
    part_one()
    part_two()
