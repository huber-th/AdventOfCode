input = [
    [40,233],
    [82,1011],
    [84,1110],
    [92,1487],
]

test = [
    [7,9],
    [15,40],
    [30,200],
]

input2 = [[40828492,233101111101487]]

test2 = [[71530,940200]]

def find_ways_to_win(races):
    wins = 1
    for race in races:
        w = 0
        for speed in range(0,race[0]):
            distance = speed * (race[0] - speed)
            if distance > race[1]:
                w += 1
        wins = wins * w
    return wins


print('part one:')
print(find_ways_to_win(input))
print('part two:')
print(find_ways_to_win(input2))
