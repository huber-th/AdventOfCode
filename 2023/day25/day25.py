""" filesystem paths module """
from pathlib import Path
from copy import deepcopy
from random import choice
from math import prod


def load_data(file: str):
    """ Load and sanitize data """
    p = Path(__file__).with_name(file)
    with p.open('r', encoding='utf8') as f:
        edges = []
        line = f.read().strip().split('\n')
        for l in line:
            source, targets = l.split(': ')
            for target in targets.split(' '):
                edges.append((source, target, source, target))

    return edges


def krager(edges, verticies: dict[str,int]):
    """ Krager's algorithm to find a cut of 3 to separate the graph in two groups """
    while(len(verticies) > 2):
        edge = choice(edges)
        removed = verticies.pop(edge[0])
        verticies[edge[1]] += removed
        edges.remove(edge)

        to_remove = []
        to_add = []
        for e in edges:
            if e[0] == edge[0]:
                to_add.append((edge[1], e[1], e[2], e[3]))
                to_remove.append(e)
            if e[1] == edge[0]:
                to_add.append((e[0], edge[1], e[2], e[3]))
                to_remove.append(e)

        for tr in to_remove:
            edges.remove(tr)
        for ta in to_add:
            if ta[0] != ta[1]:
                edges.append(ta)
    return [(e[2], e[3]) for e in edges], verticies.values()


if __name__ == '__main__':
    edges = load_data('input')
    verticies = {}

    for edge in edges:
        if edge[0] not in verticies:
            verticies[edge[0]] = 1
        if edge[1] not in verticies:
            verticies[edge[1]] = 1

    print('Part one:')
    res: int = 0
    remaining, group_sizes = [], []
    while res != 3:
        remaining, group_sizes = krager(deepcopy(edges), deepcopy(verticies))
        res = len(remaining)
    print(f'{remaining}')
    print(prod([val for val in group_sizes]))
    print('Part two:')
    print('Push the button on the website ;)')
