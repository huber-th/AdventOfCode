""" Advent of Code 2024 """
from pathlib import Path
from heapq import heappush, heappop

# Directons, R, D, L, U
directions = {(0, 1), (1, 0), (0, -1), (-1, 0)}


def load_data():
    """
    Load and sanitize data

    Return: The loaded and sanitized file content for processing
    """
    p = Path(__file__).with_name('input')
    with p.open('r', encoding='utf8') as f:
        c = [tuple(map(int, row.split(',')))
             for row in f.read().strip().split('\n')]
    return c


def draw_grid(grid):
    for row in grid:
        print()
        for tile in row:
            print(tile, end='')
    print()


def build_graph(grid):
    rows, cols = len(grid), len(grid[0])
    graph = {}

    start, end = None, None

    # Go over the grid  and build the graph of verticies
    for y in range(rows):
        for x in range(cols):
            if grid[y][x] in ('.', 'S', 'E'):
                if grid[y][x] == 'S':
                    start = (y, x)
                elif grid[y][x] == 'E':
                    end = (y, x)

                # Initialize the state for this tile
                # with all possible directions
                for dir in directions:
                    node = (y, x, dir)
                    graph[node] = {}

                    # Explore neighbours
                    for dy, dx in directions:
                        ny, nx = y + dy, x + dx

                        if nx < 0 or ny < 0 or nx >= cols or ny >= rows:
                            continue

                        if grid[ny][nx] in ('.', 'E'):
                            neighbour = (ny, nx, (dy, dx))
                            weight = 1
                            graph[node][neighbour] = weight

    return graph, start, end


def dijkstra(graph, start, end):
    """
    Find the shortest path from start to end using Dijkstra's algorithm

    https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    """

    # Priority queue to store our nodes
    pq = []

    heappush(pq, (0, start))

    visited = set()

    # Dictionary to store smallest costs for nodes
    distances = {}

    # Process until we have no nodes left to process
    while pq:
        cost, node = heappop(pq)

        if (node[0], node[1]) == end:
            return cost

        if node in visited:
            continue

        # Mark node as visited
        visited.add(node)

        ny, nx, dir = node

        # Check all directions in the graph
        for v, vc in graph[node].items():
            curr_cost = distances.get(v, float('inf'))

            new_cost = cost + vc
            if new_cost < curr_cost:
                distances[v] = new_cost
                heappush(pq, (new_cost, v))


def all():
    """ Solution Implementation for Part 1 """
    data = load_data()

    print('Part one:')
    # rows, cols = 7, 7
    # b = 12
    rows, cols = 71, 71
    b = 1024

    grid = []
    for y in range(rows):
        row = []
        for x in range(cols):
            if ((x, y)) in data[:b]:
                row.append('#')
            else:
                row.append('.')
        grid.append(row)

    grid[0][0] = 'S'
    grid[rows-1][cols-1] = 'E'
    g, s, e = build_graph(grid)
    d = dijkstra(g, (s[0], s[1], (0, 1)), e)
    print(d)

    print('Part two:')
    for x, y in data[b:len(data)]:
        grid[y][x] = '#'
        g, s, e = build_graph(grid)
        d = dijkstra(g, (s[0], s[1], (0, 1)), e)
        # Once dijkstra no longer finds a solution, we found the byte
        # after which there is no longer a path to the exit
        if not d:
            print(f'({x},{y})')
            break


if __name__ == '__main__':
    all()
