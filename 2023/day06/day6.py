from pathlib import Path

input = []

p = Path(__file__).with_name('input')
with p.open('r') as f:
    t,d = f.read().split('\n')
    x, time = t.split(':')
    time = time.strip().split(' ')
    while '' in time:
        time.remove('')
    x, distance = d.split(':')
    distance = distance.strip().split(' ')
    while '' in distance:
        distance.remove('')
    for i, t in enumerate(time):
        input.append([int(t), int(distance[i])])

print('part one:')
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

print(find_ways_to_win(input))

print('part two:')
time = ''
distance = ''
for i in input:
    time += str(i[0])
    distance += str(i[1])
print(find_ways_to_win([[int(time), int(distance)]]))
