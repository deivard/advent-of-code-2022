"""Day 7: No Space Left On Device
"""
from typing import Iterable, Tuple


class File:
    def __init__(self, name, size) -> None:
        self.name = name
        self.size = int(size)

    def get_size(self):
        return self.size


class Directory:
    def __init__(self, name, parent=None) -> None:
        self.name = name
        self.parent = parent
        self.content = {}

    def get_subdir_sizes(self):
        this_size, subdir_sizes = self.__get_subdir_sizes()
        return [this_size] + subdir_sizes

    def __get_subdir_sizes(self, sub_sizes=None):
        if sub_sizes is None:
            sub_sizes = []
        dir_size = 0
        for value in self.content.values():
            if type(value) is Directory:
                sub_dir_size, sub_sizes = value.__get_subdir_sizes(sub_sizes)
                dir_size += sub_dir_size
            elif type(value) is File:
                dir_size += value.size
        sub_sizes.append(dir_size)

        return dir_size, sub_sizes

    def get_size(self):
        total_size = 0
        for value in self.content.values():
            total_size += value.get_size()

        return total_size


def find_value_closest_to_target(iterable: Iterable, target: int):
    candidates = filter(lambda v: v >= target, iterable)
    closest_value = sorted(candidates)[0]
    return closest_value


class LineParser:
    def __init__(self) -> None:
        self.__base_directory = None
        self.__current_directory = Directory("Temporary Tree Wrapper")
        self.__current_line_index = 0
        self.__lines = []

    def create_file_tree_from_lines(self, lines: Iterable[str]):
        self.__lines = lines
        while self.__current_line_index < len(lines):
            line = lines[self.__current_line_index]
            args = self.__line_to_args(line)
            if self.__line_is_command(line):
                self.__process_command(args)
            self.__current_line_index += 1

        return self.__base_directory

    def __line_is_command(self, line: str):
        return line[0] == "$"

    def __line_to_args(self, line: str):
        return line.strip().split(" ")[1:]

    def __process_command(self, args):
        command = args[0]
        if command == "cd":
            self.__run_cd_command(args[1])
        elif command == "ls":
            self.__run_ls_command()

    def __run_cd_command(self, argument: str):
        if argument == "..":
            self.__current_directory = self.__current_directory.parent
        else:
            self.__current_directory = self.__current_directory.content.get(
                argument,
                Directory(argument, parent=self.__current_directory)
            )
        if self.__base_directory is None:
            self.__base_directory = self.__current_directory

    def __run_ls_command(self):
        i = self.__current_line_index + 1
        while (i < len(self.__lines)
               and not self.__line_is_command(self.__lines[i])):
            ls_output = self.__lines[i].strip().split(" ")
            self.__handle_ls_output(ls_output)
            i += 1
        self.__current_line_index = i - 1

    def __handle_ls_output(self, ls_output: Tuple[str, str]):
        if ls_output[0] == "dir":
            self.__current_directory.content[ls_output[1]] = Directory(
                ls_output[1], self.__current_directory
            )
        else:
            self.__current_directory.content[ls_output[1]] = File(
                ls_output[1], ls_output[0]
            )


def part_1():
    lines = open("day_07/input.txt").readlines()
    parser = LineParser()
    base_directory = parser.create_file_tree_from_lines(lines)
    subdir_sizes = base_directory.get_subdir_sizes()
    sum_of_filtered_sizes = sum(filter(lambda s: s < 100_000, subdir_sizes))
    print("Part 1 - The sum of directory sizes where the size is less than "
          f"100 000 is {sum_of_filtered_sizes}.")


def part_2():
    lines = open("day_07/input.txt").readlines()
    parser = LineParser()
    base_directory = parser.create_file_tree_from_lines(lines)
    subdir_sizes = base_directory.get_subdir_sizes()

    total_disk_space = 70_000_000
    space_required_for_update = 30_000_000
    free_space = total_disk_space - base_directory.get_size()
    additional_space_needed = (space_required_for_update-free_space)
    closest_value = find_value_closest_to_target(subdir_sizes,
                                                 additional_space_needed)
    print("Part 2 - The smallest directory that could be deleted to "
          f"free enough memory has a size of {closest_value}.")


def main():
    part_1()
    part_2()


if __name__ == "__main__":
    main()
