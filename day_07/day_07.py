
from typing import Iterable


def run_command(command: str):
    pass


def line_is_command(line: str):
    return line[0] == "$"


def line_to_args(line: str):
    return line.strip().split(" ")


class File:
    def __init__(self, name, size) -> None:
        self.name = name
        self.size = size


class Directory:
    def __init__(self, name, parent=None) -> None:
        self.name = name
        self.parent = parent
        self.content = {}


    def get_dir_sizes(self):
        dir_sizes = []
        this_size = 0
        for value in self.content.values():
            if type(value) is Directory:
                size = value.get_dir_sizes()
                dir_sizes.extend(size)
                this_size += sum(size)
            if type(value) is File:
                this_size += int(value.size)
        dir_sizes.extend([this_size])
        return dir_sizes


    def calculate_size(self):
        total_size = 0
        for value in self.content.values():
            if type(value) is Directory:
                total_size += value.calculate_size()
            if type(value) is File:
                total_size += int(value.size)
        return total_size


def find_value_closest_to_target(iterable: Iterable, target: int):
    # candidates = filter(lambda v: v >= target, iterable)
    # closest_value = sorted(candidates)[0]
    # print(list(candidates))
    # return closest_value
    closest_value = None
    for value in iterable:
        delta = target - value
        if delta < 0:
            if closest_value is None or value < closest_value:
                closest_value = value
    return closest_value


def part_1():
    base_directory = None
    current_directory = None
    ls_command_running = False
    lines = open("day_07/input.txt").readlines()
    # lines = open("day_07/test.txt").readlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        # current_line_is_command = line_is_command(line)
        if line_is_command(line):
            args = line_to_args(line)
            if args[1] == "cd":
                if args[2] == "..":
                    current_directory = current_directory.parent
                else:
                    if base_directory is None:
                        base_directory = Directory(
                            args[2],
                            parent=current_directory
                        )
                        current_directory = base_directory
                    else:
                        current_directory = current_directory.content.get(
                            args[2],
                            Directory(args[2],
                                      parent=current_directory)
                        )
                    
            if args[1] == "ls":
                ls_command_running = True
        elif ls_command_running:
            args = line_to_args(lines[i])
            if args[0] == "dir":
                current_directory.content[args[1]] = Directory(args[1],
                                                                current_directory)
            else:
                current_directory.content[args[1]] = File(args[1],
                                                            args[0])
        i += 1
        
    if base_directory is not None:
        total_size = base_directory.calculate_size()
        print(total_size)
        sizes = base_directory.get_dir_sizes()
        print(sum(filter(lambda s: s < 100_000, sizes)))
        
        total_disk_space = 70_000_000
        space_required_for_update = 30_000_000
        free_space = total_disk_space - base_directory.calculate_size()
        additional_space_needed = (space_required_for_update-free_space)
        print(sorted(sizes))
        closest_value = find_value_closest_to_target(sizes, additional_space_needed)
        print(closest_value)
        # print(size)
        # sum_size = sum(size)
        # print(sum_size)








def main():
    part_1()


if __name__ == "__main__":
    main()
