from pathlib import Path
from re import findall

def load_data(file: str):
    """ Load and sanitize data """
    p = Path(__file__).with_name(file)
    with p.open('r', encoding='utf8') as f:
        stacks, moves = f.read().split('\n\n')
        rows = stacks.replace('[',' ').replace(']',' ').split('\n')[:-1]
        stacks = [stack for stack in [list(col) for col in zip(*rows)] if not all(e == ' ' for e in stack)]
        moves = [[int(v) for v in findall(r'\d+',m)] for m in moves.split('\n')][:-1]
    return (stacks, moves)


def operate_crane_9000(stacks: list[list[str]], moves: list[list[int]]) -> list[list[str]]:
    """
    Operate the crane and move stacks around according to the moves

    Moves is a tuple of integer with the definition of count, from, to

    The crane 9000 always moves one crate at a time
    """
    for amount, from_, to in moves:
        from_ -= 1
        to -= 1
        for _ in range(amount):
            stacks[to].insert(0, (stacks[from_].pop(0)))
    return stacks


def operate_crane_9001(stacks: list[list[str]], moves: list[list[int]]) -> list[list[str]]:
    """
    Operate the crane and move stacks around according to the moves

    Moves is a tuple of integer with the definition of count, from, to

    The crane 9001 can pick up multiple crates at the same time and retains their order
    """
    for amount, from_, to in moves:
        from_ -= 1
        to -= 1
        to_move = []
        for _ in range(amount):
            to_move.insert(0, (stacks[from_].pop(0)))
        for _ in range(amount):
            stacks[to].insert(0, to_move.pop(0))
    return stacks

def get_data():
    data = load_data('input')
    s: list[list[str]] = data[0]
    m: list[list[int]] = data[1]

    for stack in s:
        while(stack[0] == ' '):
            stack.pop(0)
    return s,m


if __name__ == '__main__':

    s,m = get_data()
    print('Part one:')
    final_stacks = operate_crane_9000(s, m)
    message = ''
    for stack in final_stacks:
        message += stack[0]
    print(message)

    print('Part two:')
    s,m = get_data()
    final_stacks = operate_crane_9001(s, m)
    message = ''
    for stack in final_stacks:
        message += stack[0]
    print(message)
