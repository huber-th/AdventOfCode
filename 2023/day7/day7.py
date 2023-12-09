from pathlib import Path
from enum import IntEnum

input = []

p = Path(__file__).with_name('input')
with p.open('r') as f:
    for l in f.read().split('\n'):
        input.append(l.split(' '))

class Strength(IntEnum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 6
    FIVE_OF_A_KIND =7

class Hand:
    def __init__(self, cards: str, value: str, joker: bool = False) -> None:
        self.__cards = cards
        self.__value = int(value)
        self.__joker = joker
        if joker:
            self.analyze_cards_with_joker()
        else:
            self.analyze_cards()

    def analyze_cards(self) -> None:
        values = {}
        for card in self.__cards:
            values[card] = values.get(card, 0) + 1
        if len(values) == 5:
            self.__strength = Strength.HIGH_CARD
        if len(values) == 4:
            self.__strength = Strength.ONE_PAIR
        if len(values) == 3:
            if max(values.values()) == 2:
                self.__strength = Strength.TWO_PAIR
            else:
                self.__strength = Strength.THREE_OF_A_KIND
        if len(values) == 2:
            if max(values.values()) == 4:
                self.__strength = Strength.FOUR_OF_A_KIND
            else:
                self.__strength = Strength.FULL_HOUSE
        if len(values) == 1:
            self.__strength = Strength.FIVE_OF_A_KIND
    
    def analyze_cards_with_joker(self) -> None:
        values = {}
        jokers = 0
        for card in self.__cards:
            if card == "J":
                jokers += 1
            else:
                values[card] = values.get(card, 0) + 1
        if len(values) == 5:
            self.__strength = Strength.HIGH_CARD
        if len(values) == 4:
            self.__strength = Strength.ONE_PAIR
        if len(values) == 3:
            if jokers == 0 and max(values.values()) == 2:
                self.__strength = Strength.TWO_PAIR
            else:
                self.__strength = Strength.THREE_OF_A_KIND
        if len(values) == 2 and jokers == 0:
            if max(values.values()) == 4:
                self.__strength = Strength.FOUR_OF_A_KIND
            else:
                self.__strength = Strength.FULL_HOUSE
        if len(values) == 2 and jokers == 1:
            if max(values.values()) == 3:
                self.__strength = Strength.FOUR_OF_A_KIND
            else:
                self.__strength = Strength.FULL_HOUSE
        if len(values) == 2 and jokers == 2:
            self.__strength = Strength.FOUR_OF_A_KIND
        if len(values) == 2 and jokers == 3:
            self.__strength = Strength.FOUR_OF_A_KIND
        if len(values) == 1 or len(values) == 0:
            self.__strength = Strength.FIVE_OF_A_KIND

    def strength(self) -> int:
        return self.__strength.value

    def value(self) -> int:
        return self.__value

    def cards(self) -> str:
        return self.__cards

    def __lt__(self, other):
        if self.__strength.value == other.__strength.value:
            for i in range(0,5):
                face_value = self.determine_face_value(self.__cards[i])
                other_f_value = self.determine_face_value(other.__cards[i])
                if face_value == other_f_value:
                    continue;
                return face_value < other_f_value
        else:
            return self.__strength.value < other.__strength.value

    def determine_face_value(self, card: str) -> int:
        if card == "A":
            return 14
        if card == "K":
            return 13
        if card == "Q":
            return 12
        if card == "J":
            return 1 if self.__joker else 11
        if card == "T":
            return 10
        return int(card)

print('Part one:')
hands = []
for hand in input:
    h = Hand(hand[0], hand[1])
    hands.append(h)

hands.sort()
sum = 0
for i,h in enumerate(hands):
   sum += h.value() * (i+1)
print(sum)

print('Part two:')
hands = []
for hand in input:
    h = Hand(hand[0], hand[1], True)
    hands.append(h)

hands.sort()
sum = 0
for i,h in enumerate(hands):
   sum += h.value() * (i+1)
print(sum)