from pathlib import Path


def load_data(file: str):
    """ Load and sanitize data """
    p = Path(__file__).with_name(file)
    with p.open('r', encoding='utf8') as f:
        c = f.read().strip().split('\n')
    return c


class File:
    def __init__(self, name: str, size: int) -> None:
        self.name = name
        self.size = size


class Directory:
    def __init__(self, name: str, parent_path: str = '') -> None:
        self.name = name
        if name != '/':
            self.path = parent_path + name + '/'
        else:
            self.path = parent_path + name
        self.parent = parent_path
        self.directories: list[Directory] = []
        self.files: list[File] = []

    def add_file(self, file: File):
        self.files.append(file)

    def add_directory(self, directory: 'Directory'):
        self.directories.append(directory)

    def size(self) -> int:
        file_sizes = sum([f.size for f in self.files])
        directory_sizes = sum([d.size() for d in self.directories])
        return file_sizes + directory_sizes

    def __str__(self) -> str:
        files = [f.name for f in self.files]
        dirs = [d.name for d in self.directories]
        return f'{self.name}, files {files}, dirs {dirs} size {self.size()}'

    def get_parent(self) -> str:
        return self.parent


def print_directory_tree(dir: Directory, cur: str, lvl: int = 0):
    space = ' ' * 2 * lvl
    current = '<-----' if cur == dir.name else ''
    print(f'{space}[{lvl}] {dir.path}{current}')
    for sdir in dir.directories:
        print_directory_tree(sdir, cur, lvl + 1)


def process_terminal_output(output: list[str]) -> dict[str, Directory]:
    """
    Process the provided terminal output and find
    directories and the files contained in them.

    Sum up the size of all directories smaller than 100,000
    """
    directories: dict[str, Directory] = {}

    cur_dir: Directory | None = Directory('/')
    directories[cur_dir.name] = cur_dir
    for line in output:
        args = line.split(' ')
        if args[0] == '$':
            if args[1] == 'ls':
                continue
            if args[1] == 'cd':
                if args[2] == '..' and cur_dir is not None:
                    cur_dir = directories.get(cur_dir.get_parent())
                elif args[2] != '..' and cur_dir is not None:
                    next_dir = directories.get(args[2])
                    if next_dir is None:
                        next_dir = Directory(args[2], cur_dir.path)
                        cur_dir.add_directory(next_dir)
                        directories[next_dir.path] = next_dir
                        cur_dir = next_dir
                    else:
                        cur_dir = next_dir
                else:
                    raise Exception(f'Unsupported {line} in dir {cur_dir}')
        else:
            if args[0] == 'dir' and cur_dir is not None:
                sub_dir = directories.get(args[1])
                if sub_dir is not None:
                    cur_dir.add_directory(sub_dir)
                else:
                    sub_dir = Directory(args[1], cur_dir.path)
                    directories[sub_dir.path] = sub_dir
                    cur_dir.add_directory(sub_dir)
            elif cur_dir is not None:
                cur_dir.add_file(File(args[1], int(args[0])))
    return directories


if __name__ == '__main__':
    data = load_data('input')

    print('Part one:')
    directories = process_terminal_output(data)
    print(sum([d.size() for d in directories.values() if d.size() < 100000]))

    print('Part two:')
    disk = 70000000
    required = 30000000
    remaining = disk - directories['/'].size()
    min_to_delete = 99999999999
    for d in directories.values():
        if d.size() + remaining > required and d.size() < min_to_delete:
            min_to_delete = d.size()
    print(min_to_delete)
