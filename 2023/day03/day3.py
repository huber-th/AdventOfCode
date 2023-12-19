from pathlib import Path

input = []

p = Path(__file__).with_name('input')
with p.open('r') as f:
    lines = f.read().split('\n')
    for l in lines:
        input.append(l)

gears = {}

def add_gear(number, key):
    v = gears.get(key, None)
    if v:
        v[1] = int(number)
    else:
        v = [int(number), None]
    gears[key] = v

def verify_line(prev, l, nxt, lnumber):
    line_sum = 0
    number = ""
    in_number = False
    part_number = False
    gear = False
    key = ""
    for i, c in enumerate(l):
        if c.isnumeric():
            if in_number:
                number += c
            else:
                in_number = True
                number = c
            # only do checks for symbol if we don't know it's a part number yet
            if part_number:
                # if we are at the end add the current number
                if i == (len(l) - 1):
                    if gear:
                        add_gear(number, key)
                        gear = False
                    line_sum += int(number)
            else:
                # check left if not at the start
                if i > 0:
                    if not l[i-1].isnumeric() and l[i-1] != ".":
                        part_number = True
                        if l[i-1] == "*":
                            gear = True
                            key = '{}-{}'.format(lnumber, i-1)
                        # at the end of the line add number to sum if part_number
                        if i == (len(l) - 1):
                            if gear:
                                add_gear(number, key)
                                gear = False
                            line_sum += int(number)
                        continue
                # check left right if not at the end
                if i < len(l) - 1:
                    if not l[i+1].isnumeric() and l[i+1] != ".":
                        part_number = True
                        if l[i+1] == "*":
                            gear = True
                            key = '{}-{}'.format(lnumber, i+1)
                        if i == (len(l) - 1):
                            if gear:
                                add_gear(number, key)
                                gear = False
                            line_sum += int(number)
                        continue
                if prev:
                    if i > 0:
                        if not prev[i-1].isnumeric() and prev[i-1] != ".":
                            part_number = True
                            if prev[i-1] == "*":
                                gear = True
                                key = '{}-{}'.format(lnumber-1, i-1)
                            if i == (len(l) - 1):
                                if gear:
                                    add_gear(number, key)
                                    gear = False
                                line_sum += int(number)
                            continue
                        if not prev[i].isnumeric() and prev[i] != ".":
                            part_number = True
                            if prev[i] == "*":
                                gear = True
                                key = '{}-{}'.format(lnumber-1, i)
                            if i == (len(l) - 1):
                                if gear:
                                    add_gear(number, key)
                                    gear = False
                                line_sum += int(number)
                            continue
                        if i < len(l) - 1 and not prev[i+1].isnumeric() and prev[i+1] != ".":
                            part_number = True
                            if prev[i+1] == "*":
                                gear = True
                                key = '{}-{}'.format(lnumber-1, i+1)
                            if i == (len(l) - 1):
                                if gear:
                                    add_gear(number, key)
                                    gear = False
                                line_sum += int(number)
                            continue
                # check line above
                if nxt:
                    if i > 0:
                        if not nxt[i-1].isnumeric() and nxt[i-1] != ".":
                            part_number = True
                            if nxt[i-1] == "*":
                                gear = True
                                key = '{}-{}'.format(lnumber+1, i-1)
                            if i == (len(l) - 1):
                                if gear:
                                    add_gear(number, key)
                                    gear = False
                                line_sum += int(number)
                            continue
                        if not nxt[i].isnumeric() and nxt[i] != ".":
                            part_number = True
                            if nxt[i] == "*":
                                gear = True
                                key = '{}-{}'.format(lnumber+1, i)
                            if i == (len(l) - 1):
                                if gear:
                                    add_gear(number, key)
                                    gear = False
                                line_sum += int(number)
                            continue
                        if i < len(l) - 1 and not nxt[i+1].isnumeric() and nxt[i+1] != ".":
                            part_number = True
                            if nxt[i+1] == "*":
                                gear = True
                                key = '{}-{}'.format(lnumber+1, i+1)
                            if i == (len(l) - 1):
                                if gear:
                                    add_gear(number, key)
                                    gear = False
                                line_sum += int(number)
                            continue

        else:
            in_number = False
            if number and part_number:
                if gear:
                    add_gear(number, key)
                    gear = False
                line_sum += int(number)
                number = ""
                part_number = False
    return [line_sum]


                


sum = 0
for i,l in enumerate(input):
    if i == 0:
        prev = None
    else:
        prev = input[i-1]
    
    if i == len(input)-1:
        nxt = None
    else:
        nxt = input[i+1]
    sum += verify_line(prev,l,nxt,i)[0]

print('Part one:')
print(sum)


print('Part two:')
gear_sum = 0
for g in gears:
    if gears[g][0] and gears[g][1]:
        ratio = gears[g][0]*gears[g][1]
        gear_sum += ratio
print(gear_sum)