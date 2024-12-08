""" Advent of Code 2024 """
from pathlib import Path
import re
from itertools import combinations


def load_data():
    """
    Load and sanitize data

    Return: The loaded and sanitized file content for processing
    """
    p = Path(__file__).with_name('input')
    with p.open('r', encoding='utf8') as f:
        c = [list(line) for line in f.read().strip().split('\n')]
    return c


def print_map(map):
    """ Visualize the map for debugging if needed """
    for row in map:
        print('\n')
        for pos in row:
            print(f'{pos} ', end='')


def find_antennas(map):
    """
    Find all coordinates for antennas marked by uppercase, lowercase
    letters or digits
    """
    antennas = {}
    for y, row in enumerate(map):
        for x, pos in enumerate(row):
            if re.match(r'^[a-z]$|^[A-Z]$|^\d$', pos):
                antennas.setdefault(pos, []).append((y, x))
    return antennas


def add_antinodes_to_map(antinodes, map) -> int:
    """
    Add antinodes to map

    Return: Number of antinodes within the boundaries of the map
    """
    antinodes_in_map = 0
    for antinode in antinodes:
        if (antinode[0] >= 0 and
                antinode[1] >= 0 and
                antinode[0] < len(map) and
                antinode[1] < len(map[0])):

            antinodes_in_map += 1
            if map[antinode[0]][antinode[1]] == '.':
                map[antinode[0]][antinode[1]] = '#'
    return antinodes_in_map


def add_nodes_part2(curr, dist_y, dist_x, map) -> set:
    """
    Add all antinodes following dist_x and dist_y until we step out of the map

    Return: The list of antinodes to add
    """
    antinodes = set()

    start = curr
    antinodes.add(start)
    next = (curr[0] + dist_y, curr[1] + dist_x)
    while (next[0] >= 0 and
            next[1] >= 0 and
            next[0] < len(map) and
            next[1] < len(map[0])):
        antinodes.add((next))
        next = (next[0] + dist_y, next[1] + dist_x)
        add_antinodes_to_map(antinodes, map)

    return antinodes


def all():
    """ Solution Implementation for Part 1 """
    map = load_data()

    frequencies = find_antennas(map)
    # For each combo, find antinodes
    # Antinodes set for part 1
    antinodes = set()
    # Antinodes set for part 2
    antinodes_part2 = set()
    all_antennas = set()
    for f in frequencies:
        antennas = frequencies[f]
        all_antennas.update(antennas)
        # Find all combinations of two antennas
        combos = list(combinations(antennas, 2))

        for combo in combos:
            # Find y and x distance between the antennas
            # Use the absolute value to ensure the distance is positive
            relation_y = combo[0][0] - combo[1][0]
            relation_x = combo[0][1] - combo[1][1]
            dist_y = abs(combo[0][0] - combo[1][0])
            dist_x = abs(combo[0][1] - combo[1][1])

            # Determine the relative position of the two antennas
            # Y relation, if not equal is Point 0 below Point 1,
            # as this is how the combinations are generated by itertools
            if relation_x == 0:
                # Horizontally aligned not possible
                antinodes.add((combo[0][0] + dist_y, combo[0][1]))
                antinodes_part2.update(
                    add_nodes_part2(combo[0], dist_y, 0, map)
                )
                antinodes_part2.update(
                    add_nodes_part2(combo[0], -1 * dist_y, 0, map)
                )
                antinodes.add((combo[1][0] - dist_y, combo[1][1]))
            elif relation_x < 0:
                if relation_y == 0:
                    antinodes.add((combo[0][0], combo[0][1] - dist_x))
                    antinodes_part2.update(
                        add_nodes_part2(combo[0], 0, -1 * dist_x, map)
                    )
                    antinodes_part2.update(
                        add_nodes_part2(combo[0], 0, dist_x, map)
                    )
                    antinodes.add((combo[1][0], combo[1][1] + dist_x))
                else:
                    antinodes.add((combo[0][0] - dist_y, combo[0][1] - dist_x))
                    antinodes_part2.update(
                        add_nodes_part2(
                            combo[0], -1 * dist_y, -1 * dist_x, map
                        )
                    )
                    antinodes_part2.update(
                        add_nodes_part2(combo[0], dist_y, dist_x, map)
                    )
                    antinodes.add((combo[1][0] + dist_y, combo[1][1] + dist_x))
            else:
                if relation_y == 0:
                    antinodes.add((combo[0][0], combo[0][1] - dist_x))
                    antinodes_part2.update(
                        add_nodes_part2(combo[0], 0, -1 * dist_x, map)
                    )
                    antinodes_part2.update(
                        add_nodes_part2(combo[0], 0, dist_x, map)
                    )
                    antinodes.add((combo[1][0], combo[1][1] + dist_x))
                else:
                    antinodes.add((combo[1][0] + dist_y, combo[1][1] - dist_x))
                    antinodes_part2.update(
                        add_nodes_part2(combo[1], dist_y, -1 * dist_x, map)
                    )
                    antinodes_part2.update(
                        add_nodes_part2(combo[1], -1 * dist_y, dist_x, map)
                    )
                    antinodes.add((combo[0][0] - dist_y, combo[0][1] + dist_x))

    added = add_antinodes_to_map(antinodes, map)
    print('Part one:')
    print(added)
    print('Part two:')
    print(len(antinodes_part2))


if __name__ == '__main__':
    all()
