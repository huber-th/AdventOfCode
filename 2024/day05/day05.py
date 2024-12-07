""" Advent of Code 2024 """
from pathlib import Path


def load_data():
    """
    Load and sanitize data

    Return: The loaded and sanitized file content for processing
    """
    p = Path(__file__).with_name('input')
    with p.open('r', encoding='utf8') as f:
        rules, updates = f.read().strip().split('\n\n')
        rules = [list(rule.split('|')) for rule in rules.split('\n')]
        updates = [list(update.split(',')) for update in updates.split('\n')]
    return rules, updates


def is_valid_update(rules, update):
    seen = []
    for num in update:
        rule_targets = [rule[1] for rule in rules if rule[0] == num]
        if any(rule_target in seen for rule_target in rule_targets):
            return False
        seen.append(num)
    return True


def validate_updates(rules, updates):
    valid_updates = []
    invalid_updates = []
    for update in updates:
        if is_valid_update(rules, update):
            valid_updates.append(update)
        else:
            invalid_updates.append(update)
    return valid_updates, invalid_updates


def correct_update(rules, invalid_updates):
    corrected_updates = []

    for update in invalid_updates:
        # Loop over each number in the invalid update
        while not is_valid_update(rules, update):
            corrected_update = []
            for i, num in enumerate(update):
                # Find the targets for the index
                rule_targets = [rule[1] for rule in rules if rule[0] == num]
                append = True
                for target in rule_targets:
                    if target in corrected_update:
                        corrected_update.insert(
                            corrected_update.index(target), num)
                        append = False
                        break
                if append:
                    corrected_update.append(num)
            update = corrected_update
        corrected_updates.append(update)
    return corrected_updates


def part_one():
    """ Solution Implementation for Part 1 """
    rules, updates = load_data()

    print('Part one:')
    valid_updates, invalid_updates = validate_updates(rules, updates)

    result = 0
    for valid_update in valid_updates:
        result += int(valid_update[len(valid_update) // 2])
    print(result)


def part_two():
    """ Solution Implementation for Part 2 """
    rules, updates = load_data()
    print('Part two:')

    valid_updates, invalid_updates = validate_updates(rules, updates)
    corrected_updates = correct_update(rules, invalid_updates)

    result = 0
    for valid_update in corrected_updates:
        result += int(valid_update[len(valid_update) // 2])
    print(result)


if __name__ == '__main__':
    part_one()
    part_two()
