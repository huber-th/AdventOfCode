""" Advent of Code 2024 """
from pathlib import Path
from heapq import heappush, heappop


def load_data():
    """
    Load and sanitize data

    Return: The loaded and sanitized file content for processing
    """
    p = Path(__file__).with_name('input')
    with p.open('r', encoding='utf8') as f:
        c = [list(row) for row in f.read().strip().split('\n')]
    return c


def draw_map(map):
    for row in map:
        print()
        for tile in row:
            print(tile, end='')
    print()


def find_start(map):
    for y, row in enumerate(map):
        for x, tile in enumerate(row):
            if tile == 'S':
                return (y, x)
    return None


def find_target(map):
    for y, row in enumerate(map):
        for x, tile in enumerate(row):
            if tile == 'E':
                return (y, x)
    return None


# Directons, R, D, L, U
directions = {(0, 1), (1, 0), (0, -1), (-1, 0)}


def build_graph_with_turns(grid):
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

                        if grid[ny][nx] in ('.', 'E'):
                            neighbour = (ny, nx, (dy, dx))
                            # Weight 1 if same direction, 1001 otherwise
                            if dir == (dy, dx):
                                weight = 1
                            else:
                                weight = 1001
                            graph[node][neighbour] = weight

    return graph, start, end


def dijkstra(graph, start, end):
    """
    Find the shortest path from start to end using Dijkstra's algorithm

    https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    """

    # Priority queue to store our nodes
    pq = []

    heappush(pq, (0, start, [start]))

    visited = set()

    # Dictionary to store smallest costs for nodes
    distances = {}

    # Dictionary to store previous nodes for smallest paths
    previous = {}

    # Process until we have no nodes left to process
    while pq:
        cost, node, prev = heappop(pq)

        if (node[0], node[1]) == end:
            return cost, prev, previous

        if node in visited:
            continue

        # Mark node as visited
        visited.add(node)

        ny, nx, dir = node

        # Check all directions in the graph
        for v, vc in graph[node].items():
            curr_cost = distances.get(v, float('inf'))

            new_cost = cost + vc
            # Part 2, if the cost is the same as the smallest, add the node
            # to the previous node list to count how many nodes are on
            # any smallest path
            if new_cost == curr_cost:
                previous[v].append(node)
                heappush(pq, (new_cost, v, previous[v]))
            if new_cost < curr_cost:
                distances[v] = new_cost
                previous[v] = [node]
                heappush(pq, (new_cost, v, previous[v]))


def count_nodes_on_smallest_paths(curr, graph, unique_nodes):
    """
    Follow the previous nodes from start and determine how many nodes are
    on the path
    """

    for n in curr:
        if n not in graph:
            return
        unique_nodes.add((n[0], n[1]))
        count_nodes_on_smallest_paths(graph[n], graph, unique_nodes)
    return unique_nodes


def all():
    """ Solution Implementation for Part 1 """
    grid = load_data()

    print('Part one:')
    graph, start, end = build_graph_with_turns(grid)
    dist, prev, prev_dict = dijkstra(graph, (start[0], start[1], (0, 1)), end)
    print(dist)

    print('Part two:')
    unique_nodes = {start, end}
    nodes = count_nodes_on_smallest_paths(prev, prev_dict, unique_nodes)
    print(len(nodes))


if __name__ == '__main__':
    all()
