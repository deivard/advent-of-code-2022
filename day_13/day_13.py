"""Day 13: Distress Signal
"""
from ast import literal_eval
from functools import cmp_to_key
from typing import Any


def parse_file(filename: str):
    pairs = open(filename).read().split("\n\n")
    parsed_pairs = []

    for pair in pairs:
        first, second = pair.split("\n")
        parsed_pairs.append((literal_eval(first.strip()),
                            literal_eval(second.strip())))
    return parsed_pairs


def compare(left_iter, right_iter):
    while True:
        left = next(left_iter, None)
        right = next(right_iter, None)

        # Both lists ran out of items and no check has made a decision
        if left is None and right is None:
            return None

        # Exactly one value is an integer
        if type(left) is not type(right):
            if type(left) is int:
                left = [left]
            if type(right) is int:
                right = [right]

        # Left list is shorter -> right order
        if left is None and right is not None:
            return True
        # Right list is shorter -> wrong order
        elif right is None and left is not None:
            return False

        # Both values are integers
        if type(left) is int and type(right) is int:
            if left == right:
                continue
            elif left < right:
                return True
            else:
                return False

        # Both values are lists
        elif type(left) is list and type(right) is list:
            correct_order = compare(iter(left), iter(right))
            if correct_order is None:
                continue
            else:
                return correct_order


def order_is_correct(left: list[int], right: list[int]):
    return compare(iter(left), iter(right))


def sort_compare(left: list[Any], right: list[Any]):
    correct_order = compare(iter(left), iter(right))
    return -1 if correct_order else 1


def get_packet_indices(sorted_packets: list[Any], packets: list[list[Any]]):
    decoder_keys_indices = []
    for i, packet in enumerate(sorted_packets):
        if packet in packets:
            decoder_keys_indices.append(i+1)
    return decoder_keys_indices


def part_1():
    pairs = parse_file("day_13/input.txt")
    index_of_correct_orders = []
    for index, pair in enumerate(pairs):
        if order_is_correct(pair[0], pair[1]):
            index_of_correct_orders.append(index+1)

    print("Part 1 - The sum of the indices where the orders are correct is "
          f"{sum(index_of_correct_orders)}")


def part_2():
    divider_packets = [[[2]], [[6]]]
    pairs = parse_file("day_13/input.txt")
    pairs.append(divider_packets)
    packets = []
    for pair in pairs:
        packets.extend(pair)
    sorted_packets = sorted(packets, key=cmp_to_key(sort_compare))
    indices = get_packet_indices(sorted_packets, divider_packets)

    print("Part 2 - The product of the divider packet indices is "
          f"{indices[0]*indices[1]}")


def main():
    part_1()
    part_2()


if __name__ == "__main__":
    main()
