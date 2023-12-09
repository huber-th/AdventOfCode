from pathlib import Path

input = []

p = Path(__file__).with_name('input')
with p.open('r') as f:
    lines = f.read().split('\n')
    for l in lines:
        input.append(l)

def sanitize_card(card):
    r_trimmed = card.split(":")
    card = r_trimmed[1].split("|")
    winners = card[0].strip().split(" ")
    numbers = card[1].strip().split(" ")
    # remove empty entries
    while("" in winners):
        winners.remove("")
    while("" in numbers):
        numbers.remove("")
    return [winners, numbers]

def get_card_value(winning_numbers):
    return 2**(len(winning_numbers)-1)

def parse_cards(cards):
    sum = 0
    for card in cards:
        card = sanitize_card(card)
        winning_numbers = [ e for e in card[0] if e in card[1] ]
        if (len(winning_numbers) > 0):
            sum += get_card_value(winning_numbers)
    return sum


def parse_card_recursive(idx, cards):
    sum = 1
    card = sanitize_card(cards[idx])
    winning_numbers = [ e for e in card[0] if e in card[1] ]
    print(int(idx/len(cards)*100),"         percent complete", end="\r"),
    for j in range(1, len(winning_numbers)+1):
        next = idx+j
        if len(cards) > next:
            sum += parse_card_recursive(next, cards)
    return sum

def parse_cards_recursive(cards):
    sum = 0
    for i in range(len(cards)):
        sum += parse_card_recursive(i, cards)
    return sum

print('Part one:')
print(parse_cards(input))


print('Part two:')
print(parse_cards_recursive(input), "                         ")
