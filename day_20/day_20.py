"""Day 20: Grove Positioning System
"""

from copy import deepcopy


def parse_input(filename: str):
    return [int(line.strip())
            for line in open(filename).readlines()]


def uniqueify(sequence):
    return [(index, value) for index, value in enumerate(sequence)]


def wrap_red(string):
    return f"\033[0;31m{string}\033[0m"


def wrap_green(string):
    return f"\033[0;32m{string}\033[0m"


def print_comparison(sequence, iteration):
    correct_orders = [
        [1, 2, -3, 3, -2, 0, 4],
        [2, 1, -3, 3, -2, 0, 4],
        [1, -3, 2, 3, -2, 0, 4],
        [1, 2, 3, -2, -3, 0, 4],
        [1, 2, -2, -3, 0, 3, 4],
        [1, 2, -3, 0, 3, 4, -2],
        [1, 2, -3, 0, 3, 4, -2],
        [1, 2, -3, 4, 0, 3, -2]
    ]
    sequence = [e[1] for e in sequence]
    combined = zip(sequence, correct_orders[iteration])
    correction_string = ""
    colored_string = ""
    for value, correct in combined:
        if value != correct:
            colored_string += wrap_red(value).rjust(14)
            correction_string += str(correct).rjust(3)
        else:
            colored_string += wrap_green(value).rjust(14)
            correction_string += f"{' '.rjust(3)}"

    print(correction_string)
    print(colored_string)


def find_index_of_0(uniqueified):
    for i in range(len(uniqueified)):
        if uniqueified[i][1] == 0:
            return i
    raise ValueError("0 is not present in the list.")


def part_1():
    sequence = parse_input("day_20/input.txt")
    uniqueified = uniqueify(sequence)
    mixing_order = deepcopy(uniqueified)
    for value in mixing_order:
        shift_amount = value[1]
        if shift_amount:
            index = uniqueified.index(value)
            uniqueified.pop(index)
            new_index = (index+shift_amount) % len(uniqueified)
            if new_index == 0 and shift_amount < 0:
                new_index = len(uniqueified)

            uniqueified.insert(new_index, value)

    index_of_0 = find_index_of_0(uniqueified)
    index_1000 = uniqueified[(index_of_0 + 1000) % len(uniqueified)][1]
    index_2000 = uniqueified[(index_of_0 + 2000) % len(uniqueified)][1]
    index_3000 = uniqueified[(index_of_0 + 3000) % len(uniqueified)][1]
    index_sum = sum([index_1000, index_2000, index_3000])
    print(f"Part 1 - 1000th index: {index_1000}\n"
          f"         2000th index: {index_2000}\n"
          f"         3000th index: {index_3000}\n"
          f"         Sum of values at specified indices: {index_sum}")


def part_2():
    decryption_key = 811589153
    sequence = parse_input("day_20/input.txt")
    uniqueified = uniqueify(sequence)
    uniqueified = [(i, value*decryption_key) for i, value in uniqueified]

    mixing_order = deepcopy(uniqueified)
    for _ in range(10):
        for value in mixing_order:
            shift_amount = value[1]
            if shift_amount:
                index = uniqueified.index(value)
                uniqueified.pop(index)
                new_index = (index+shift_amount) % len(uniqueified)
                if new_index == 0 and shift_amount < 0:
                    new_index = len(uniqueified)

                uniqueified.insert(new_index, value)

    index_of_0 = find_index_of_0(uniqueified)
    index_1000 = uniqueified[(index_of_0 + 1000) % len(uniqueified)][1]
    index_2000 = uniqueified[(index_of_0 + 2000) % len(uniqueified)][1]
    index_3000 = uniqueified[(index_of_0 + 3000) % len(uniqueified)][1]
    index_sum = sum([index_1000, index_2000, index_3000])
    print(f"Part 2 - 1000th index: {index_1000}\n"
          f"         2000th index: {index_2000}\n"
          f"         3000th index: {index_3000}\n"
          f"         Sum of values at specified indices: {index_sum}")


def main():
    part_1()
    part_2()


if __name__ == "__main__":
    main()
