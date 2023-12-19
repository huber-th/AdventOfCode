from pathlib import Path

data = []

p = Path(__file__).with_name('input')
with p.open('r') as f:
    line = f.read().strip().split('\n')
    for entry in line:
        values = []
        for e in entry.split(' '):
            values.append(int(e))
        data.append(values)

def build_tree(values):
    rows = []
    done = False
    curr = values
    rows.append(values)

    while not done:
        done = True
        nxt = []
        for i in range(1, len(curr)):
            val = curr[i]-curr[i-1]
            nxt.append(val)
            if val != 0:
                done = False
        rows.append(nxt)
        curr = nxt
    return rows

def find_next_value_right(rows):
    val = rows[-2][-1] + rows[-1][-1]
    for i in reversed(range(0,len(rows)-2)):
        val = rows[i][-1] + val
    return val

def find_next_value_left(rows):
    val = rows[-2][0] + rows[-1][0]
    for i in reversed(range(0,len(rows)-2)):
        val = rows[i][0] - val
    
    return val

sum = 0
for d in data:
    sum += find_next_value_right(build_tree(d))
print('Part one:')
print(sum)

sum = 0
for d in data:
    sum += find_next_value_left(build_tree(d))
print('Part two:')
print(sum)