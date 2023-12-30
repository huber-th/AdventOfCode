""" filesystem paths module """
from pathlib import Path


def load_data(file: str):
    """ Load and sanitize data """
    p = Path(__file__).with_name(file)
    with p.open('r', encoding='utf8') as f:
        return f.read().strip().split('\n')


def find_duplicate_item(rucksack: str) -> str:
    """
    Find the duplicate item in the rucksack.

    The rucksack has two compartments. Splitting the rucksack
    string in half gives us the first and second compartment.

    Then we have to find which letter is in both
    """
    first, second = rucksack[:len(rucksack)//2], rucksack[len(rucksack)//2:] 
    duplicate_item = ''.join(set(first).intersection(second))
    return duplicate_item


def item_priority(item: str) -> int:
    """
    Determine the item value

    Lowercase item types a through z have priorities 1 through 26.
    Uppercase item types A through Z have priorities 27 through 52.
    """
    priority = ord(item)

    # Adjust ASCII value to the above mentioned priority
    if priority < 97:
        priority -= 64 - 26
    else:
        priority -= 96
    return priority


def find_common_item(rucksacks: list[str]) -> str:
    """
    Find the common item between the rucksacks.

    Each letter is a single item. Find which letter appears
    in all input strings.
    """
    common_items = rucksacks[0]
    for rucksack in rucksacks[1:]:
        common_items = ''.join(set(common_items).intersection(rucksack))
    return common_items

if __name__ == '__main__':
    rucksacks = load_data('input')

    print('Part one:')
    result: int = 0
    for rucksack in rucksacks:
        item = find_duplicate_item(rucksack)
        result += item_priority(item)
    print(result)

    print('Part two:')
    list_of_groups = zip(*(iter(rucksacks),) * 3)
    result: int = 0
    for group in list_of_groups:
        common_item = find_common_item(group)
        result += item_priority(common_item)
    print(result)
