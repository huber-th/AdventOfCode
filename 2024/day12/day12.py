""" Advent of Code 2024 """
from pathlib import Path


# Directions R, D, L, U
directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def load_data():
    """
    Load and sanitize data

    Return: The loaded and sanitized file content for processing
    """
    p = Path(__file__).with_name('input')
    with p.open('r', encoding='utf8') as f:
        c = [list(rows) for rows in f.read().strip().split('\n')]
    return c


def print_map(map):
    """
    Print map for visualization
    """
    for row in map:
        print()
        for field in row:
            print(field, end='')


def explore_region(curr, plot, map, seen):
    """
    Explore the map and find all connected plots that make up the region
    """
    if curr in seen:
        return []

    seen.add(curr)
    region = [curr]

    for d in directions:
        nxt = (curr[0] + d[0], curr[1] + d[1])

        # Validate we are within the map
        if (nxt[0] < 0 or nxt[1] < 0 or
                nxt[0] >= len(map) or nxt[1] >= len(map[0])):
            continue
        # Validate if the nxt tile is of the same garden plot
        if map[nxt[0]][nxt[1]] != plot:
            continue

        region.extend(explore_region(nxt, plot, map, seen))

    return region


def find_regions(map):
    """
    Find all regions identified by the same letter.
    """
    # All regions we have found
    regions = []
    # All tiles we have already assigned to a region
    seen = set()

    for y, row in enumerate(map):
        for x, tile in enumerate(row):
            if (y, x) not in seen:
                regions.append([tile, explore_region((y, x), tile, map, seen)])

    return regions


def count_perimeter(tile, region):
    """
    Count the perimeter
    """
    sides = 0

    # To find the outside edges we can go over all tiles and count how many
    # neighbouring tiles are not in our region
    for d in directions:
        nxt = (tile[0] + d[0], tile[1] + d[1])
        if nxt not in region:
            sides += 1

    return sides


def count_corners(region: set) -> int:
    # Outside corners:
    # Example: top left outside corner
    # ?.   # If (y-1, x) (up) and (y, x-1) (left) are different from A
    # .A<  # Then A is an outside corner

    # Inside corners:
    # Example: top left inside corner
    # VA   # if (y-1, x) and (y, x-1) are the same
    #      # and (y-1, x-1) is different from A,
    # AA<  # then A is an inside corner

    # Check each possible corner of each tile
    # A single coordinate can be a corner up to 4 times

    outside_corners = [
        # different, different
        [(0, -1), (-1, 0)],  # left top
        [(0, -1), (1, 0)],   # left bottom
        [(1, 0), (0, 1)],  # right bottom
        [(-1, 0), (0, 1)]  # right top
    ]
    inside_corners = [
        # Same, same, different
        [(0, -1), (-1, 0), (-1, -1)],
        [(0, -1), (1, 0), (1, -1)],
        [(1, 0), (0, 1), (1, 1)],
        [(-1, 0), (0, 1), (-1, 1)]
    ]
    corner_count = 0
    for coord in region:
        cx, cy = coord
        for oc in outside_corners:
            ox1, oy1 = oc[0]
            ox2, oy2 = oc[1]
            if (
                (cx + ox1, cy + oy1) not in region and
                    (cx + ox2, cy + oy2) not in region):
                corner_count += 1
        for ic in inside_corners:
            ox1, oy1 = ic[0]
            ox2, oy2 = ic[1]
            ox3, oy3 = ic[2]
            if (
                (cx + ox1, cy + oy1) in region and
                    (cx + ox2, cy + oy2) in region and
                    (cx + ox3, cy + oy3) not in region):
                corner_count += 1
    return corner_count


def part_one():
    """ Solution Implementation for Part 1 """
    map = load_data()

    print('Part one:')
    total_price = 0
    regions = find_regions(map)
    for region in regions:
        sides = 0
        tiles = 0
        for t in region[1]:
            tiles += 1
            sides += count_perimeter(t, region[1])
        total_price += tiles * sides
        # print(f'{region[0]} has {tiles} tiles and {sides} sides')
    print(total_price)


def part_two():
    """ Solution Implementation for Part 2 """
    map = load_data()

    print('Part two:')
    total_price = 0
    regions = find_regions(map)
    for region in regions:
        edges = 0
        tiles = 0
        for t in region[1]:
            tiles += 1
        edges = count_corners(region[1])
        total_price += tiles * edges
    print(total_price)


if __name__ == '__main__':
    part_one()
    part_two()
