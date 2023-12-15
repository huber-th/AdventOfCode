""" filesystem paths module """
from pathlib import Path


def load_data(file: str):
    """ Load and sanitize data """
    p = Path(__file__).with_name(file)
    with p.open('r', encoding='utf8') as f:
        c = f.read().strip().split(',')
    return c


class Lense:
    """ Class representing a lense """

    def __init__(self, label: str, focal: int) -> None:
        self.label = label
        self.focal = focal
        self.hash = self.calculate_hash(label, 0)

    def __str__(self):
        return f'{self.label} with focal {self.focal}'

    def calculate_hash(self, seq: str, init: int):
        """ Calcualte the hash """
        res = init
        for c in seq:
            res += ord(c)
            res *= 17
            res %= 256
        return res

    def get_hash(self) -> str:
        """ Get the lense hash"""
        return self.hash

    def get_label(self) -> str:
        """ Return the label of the lense """
        return self.label

    def get_focal(self) -> int:
        """ Return the focal of the lense """
        return self.focal


class Box:
    """ Class representing a box """

    def __init__(self) -> None:
        self.lenses = []

    def add_lense(self, new_lense: Lense) -> None:
        """ Add a lense to the end of the box """
        replaced = False
        for i, l in enumerate(self.lenses):
            if l.get_label() == new_lense.get_label():
                self.lenses[i] = new_lense
                replaced = True
        if not replaced:
            self.lenses.append(new_lense)

    def remove_lense(self, lense_to_remove: Lense) -> None:
        """ Remove the lense with the matching label """
        self.lenses = [l for l in self.lenses if l.label !=
                       lense_to_remove.get_label()]

    def get_combined_focusing_power(self, box_number: int) -> int:
        """
        Get the combined focusing power of the box
        """
        fp: int = 0
        for slot, l in enumerate(self.lenses, 1):
            fp += (box_number + 1) * slot * l.get_focal()
        return fp

    def __str__(self) -> str:
        s = ''
        for l in self.lenses:
            s += f'[{l.get_label()} {l.get_focal()}]'
        return s


if __name__ == '__main__':
    data = load_data('input')

    print('Part one:')
    result: int = 0
    for sequence in data:
        result += Lense(sequence, 0).get_hash()
    print(result)

    print('Part two:')
    boxes = []
    for i in range(0, 256):
        boxes.append(Box())
    for sequence in data:
        if '=' in sequence:
            split = sequence.split('=')
            lense: Lense = Lense(split[0], int(split[1]))
            boxes[lense.get_hash()].add_lense(lense)
        if '-' in sequence:
            label_to_remove = sequence.split('-')[0]
            lense = Lense(label_to_remove, 0)
            boxes[lense.get_hash()].remove_lense(lense)
    result: int = 0
    for i, box in enumerate(boxes):
        result += box.get_combined_focusing_power(i)
    print(result)
