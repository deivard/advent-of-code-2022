"""Day 11: Monkey in the Middle
"""
from collections import deque
from math import prod
import operator


class Monkey:
    def __init__(self, possesions: deque, operation: dict,
                 condition: int, linked_monkeys: dict) -> None:
        self.possesions = possesions
        self.condition = condition
        self.operation = operation
        self.linked_monkeys = linked_monkeys
        self.activity_level = 0

    def calculate_new_worry_level(self, old_value: int,
                                  magic_modulo_number: int = ((2**64) - 1)):
        operator_mappings = {
            "*": operator.mul,
            "+": operator.add,
            "-": operator.sub,
            "/": operator.truediv
        }
        op = self.operation
        a = old_value if op["terms"][0] == "old" else int(op["terms"][0])
        b = old_value if op["terms"][1] == "old" else int(op["terms"][1])
        return operator_mappings[op["operator"]](a, b) % magic_modulo_number

    def conduct_test(self, worry_level: int) -> bool:
        return worry_level % self.condition == 0


def find_line_that_starts_with(starting_str: str, lines: str):
    for line in lines:
        line = line.strip()
        if line.startswith(starting_str):
            return line
    raise ValueError("Could not find line that starts with "
                     f"\"{starting_str}\"")
    

def get_monkey_index_from_lines(lines: list[str]) -> int:
    line = find_line_that_starts_with("Monkey", lines)
    return int(line.split(" ")[-1].replace(":", ""))


def get_possesions_from_lines(lines: list[str]) -> deque:
    line = find_line_that_starts_with("Starting items", lines)
    items_list = (line
                  .replace("Starting items: ", "")
                  .strip()
                  .replace(" ", "")
                  .split(","))
    return deque([int(item) for item in items_list])


def get_operation_from_lines(lines: list[str]) -> dict:
    line = find_line_that_starts_with("Operation", lines)
    operation = (line
                 .replace("Operation: new =", "")
                 .strip()
                 .split(" "))
    return {
        "terms": [operation[0], operation[2]],
        "operator": operation[1]
    }


def get_divisble_value_from_lines(lines: list[str]) -> int:
    line = find_line_that_starts_with("Test:", lines)
    divisible_by = int(line.split(" ")[-1].strip())
    return divisible_by


def get_linked_monkeys_from_lines(lines: list[str]) -> dict:
    true_line = find_line_that_starts_with("If true:", lines)
    false_line = find_line_that_starts_with("If false:", lines)
    return {
        "true_monkey": int(true_line.split(" ")[-1]),
        "false_monkey": int(false_line.split(" ")[-1])
    }


def create_monkeys_from_input_file(filename: str) -> dict[Monkey]:
    input_str = open(filename).read()
    monkey_blocks = input_str.split("\n\n")
    monkeys = [None] * len(monkey_blocks)
    for block in monkey_blocks:
        block_lines = block.split("\n")
        monkeys[get_monkey_index_from_lines(block_lines)] = Monkey(
            possesions=get_possesions_from_lines(block_lines),
            operation=get_operation_from_lines(block_lines),
            condition=get_divisble_value_from_lines(block_lines),
            linked_monkeys=get_linked_monkeys_from_lines(block_lines)
        )

    return monkeys


def get_monkey_activity_levels(monkeys: list) -> int:
    return [monkey.activity_level for monkey in monkeys]


def calculate_monkey_business_level(activity_levels: list[int]) -> int:
    activity_levels_sorted = sorted(activity_levels)
    return activity_levels_sorted[-1] * activity_levels_sorted[-2]


def part_1():
    monkeys = create_monkeys_from_input_file("day_11/input.txt")
    rounds = 20
    for _ in range(rounds):
        for monkey in monkeys:
            while len(monkey.possesions):
                item = monkey.possesions.popleft()
                monkey.activity_level += 1
                new_item_worry_level = monkey.calculate_new_worry_level(item)
                new_item_worry_level = new_item_worry_level // 3
                test_result = monkey.conduct_test(new_item_worry_level)
                if test_result is True:
                    target_monkey = monkey.linked_monkeys["true_monkey"]
                else:
                    target_monkey = monkey.linked_monkeys["false_monkey"]
                monkeys[target_monkey].possesions.append(new_item_worry_level)

    activity_levels = get_monkey_activity_levels(monkeys)
    monkey_business_level = calculate_monkey_business_level(activity_levels)
    print("The monkey business level after 20 rounds is "
          f"{monkey_business_level}.")


def part_2():
    monkeys = create_monkeys_from_input_file("day_11/input.txt")
    very_big_brain_mathematic_modulo_number = prod(
        [monkey.condition for monkey in monkeys]
    )
    rounds = 10_000
    for _ in range(rounds):
        for monkey in monkeys:
            while len(monkey.possesions):
                item = monkey.possesions.popleft()
                monkey.activity_level += 1
                new_item_worry_level = monkey.calculate_new_worry_level(
                    item, very_big_brain_mathematic_modulo_number
                )
                test_result = monkey.conduct_test(new_item_worry_level)
                if test_result is True:
                    target_monkey = monkey.linked_monkeys["true_monkey"]
                else:
                    target_monkey = monkey.linked_monkeys["false_monkey"]
                monkeys[target_monkey].possesions.append(new_item_worry_level)

    activity_levels = get_monkey_activity_levels(monkeys)
    monkey_business_level = calculate_monkey_business_level(activity_levels)
    print("The monkey business level after 10 000 rounds is "
          f"{monkey_business_level}.")


def main():
    part_1()
    part_2()


if __name__ == "__main__":
    main()
