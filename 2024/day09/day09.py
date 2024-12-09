""" Advent of Code 2024 """
from pathlib import Path


def load_data():
    """
    Load and sanitize data

    Return: The loaded and sanitized file content for processing
    """
    p = Path(__file__).with_name('input')
    with p.open('r', encoding='utf8') as f:
        c = list(map(int, f.read().strip()))
    return c


def read_checksum(checksum):
    """ Read the checksum and determine file blocks and free space """
    file_id = 0
    file = True
    filesystem = []
    for i, pos in enumerate(checksum):
        if file:
            file = False
            filesystem.extend([file_id] * pos)
            file_id += 1
        else:
            file = True
            filesystem.extend(['.'] * pos)
    return filesystem


def is_optimized(fs):
    """
    Check if the files are continuous without free space
    """
    found_file = False
    for c in reversed(fs):
        if c != '.':
            found_file = True
        else:
            if found_file:
                return False
    return True


def reorganize_files(fs):
    """
    Re-organize the file system by moving files from the end to the first
    free spot.
    """

    # Find all free spots
    free = [i for i, c in enumerate(fs) if c == '.']

    # Iterate backwards over the fs and move files
    moved = 0
    for i, c in enumerate(reversed(fs)):
        # Calculate the index in the array we are at
        idx = len(fs) - i - 1
        if c != '.':
            fs[free.pop(0)] = c
            fs[idx] = '.'
            moved += 1
        if len(free) == 0:
            break
        if is_optimized(fs):
            break
    return fs


def has_block_of_length_n(free, n):
    """
    Check if there are numbers in the free list
    which are consecutive for n blocks

    Return: the first index of the first spot in free fitting block of n-blocks
    """
    for i in range(len(free) - n + 1):
        if free[i + n - 1] - free[i] == n - 1:
            return i
    return - 1


def reorganize_file_blocks(fs):
    """
    Re-organize the file system by moving complete file blocks to the
    first spot which fits them
    """

    # Find all free spots
    free = [i for i, c in enumerate(fs) if c == '.']

    file_id = None
    length = 0
    for i, c in enumerate(reversed(fs[1:])):
        # Calculate the index in the array we are at
        idx = len(fs) - i - 1
        if c == '.':
            file_id = None
        else:
            if file_id is None:
                file_id = c
            length += 1
            if fs[idx - 1] != file_id:
                # File block complete, let's see if there is free space
                free_idx = has_block_of_length_n(free, length)
                if free_idx > -1 and free[free_idx] < idx:
                    # Free space found before current index in the filesystem
                    new_positions = []
                    for k in range(free_idx, free_idx + length):
                        new_positions.append(free.pop(free_idx))
                    for pos in new_positions:
                        fs[pos] = file_id
                    for j in range(length):
                        fs[idx + j] = '.'
                file_id = None
                length = 0
    return fs


def part_one():
    """ Solution Implementation for Part 1 """
    data = load_data()
    fs = read_checksum(data)
    organized = reorganize_files(fs)

    print('Part one:')
    res = 0
    pos = 0
    for c in organized:
        if c == '.':
            break
        res += pos * c
        pos += 1
    print(res)


def part_two():
    """ Solution Implementation for Part 2 """
    data = load_data()
    fs = read_checksum(data)
    organized = reorganize_file_blocks(fs)

    # print('Part two:')
    res = 0
    for i, c in enumerate(organized):
        if c == '.':
            continue
        res += i * c
    print(res)


if __name__ == '__main__':
    part_one()
    part_two()
