import re
from pathlib import Path

input = []

p = Path(__file__).with_name('input')
with p.open('r') as f:
    input = f.read().split('\n')

sum = 0
for s in input:
    s = re.sub("[^0-9]", "", s)
    val = '{}{}'.format(s[0], s[len(s)-1])
    sum += int(val)
print('Part one:')
print(sum)

def getDigit(s):
    if s == "one":
        return 1
    if s == "two":
        return 2
    if s == "three":
        return 3
    if s == "four":
        return 4
    if s == "five":
        return 5
    if s == "six":
        return 6
    if s == "seven":
        return 7
    if s == "eight":
        return 8
    if s == "nine":
        return 9

def getFirstWordNumberIndex(input):
    min = 100
    digit = 0
    for s in ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]:
        v = input.find(s)
        if v > -1 and v < min:
            min = v
            digit = getDigit(s)
    return [min, digit] if min != 100 else None

def getLastWordNumberIndex(input):
    max = -1
    digit = 0
    for s in ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]:
        v = input.rfind(s)
        if v > -1 and v > max:
            max = v
            digit = getDigit(s)
    return [max,digit] if max > -1 else None

def findFirstDigitIndex(s):
    for i, c in enumerate(s):
        if c.isdigit():
            return [i, s[i]]
    return None

def findLastDigitIndex(s):
    for i, c in enumerate(reversed(s)):
        if c.isdigit():
            return [len(s)-1-i, s[len(s)-1-i]]
    return None

sum = 0
for s in input:
    wmin = getFirstWordNumberIndex(s)
    wmax = getLastWordNumberIndex(s)
    dmin = findFirstDigitIndex(s)
    dmax = findLastDigitIndex(s)

    fd = 0
    ld = 0
    if wmin is None:
        fd = dmin[1]
    else:
        fd = wmin[1] if wmin[0] < dmin[0] else dmin[1]

    if wmax is None:
        ld = dmax[1]
    else:
        ld = wmax[1] if wmax[0] > dmax[0] else dmax[1]

    val = '{}{}'.format(fd, ld)
    sum += int(val)
print('Part two:')
print(sum)