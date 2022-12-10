"""Day 9: Rope Bridge
"""
from typing import Iterable


STEP_VECTORS = {
    "R":  (1, 0),    # Right
    "L":  (-1, 0),   # Left
    "U":  (0, 1),    # Up
    "D":  (0, -1),   # Down
    "LU": (-1, 1),   # Left up
    "RU": (1, 1),    # Right up
    "LD": (-1, -1),  # Left down
    "RD": (1, -1),   # Right down
    "NO": (0, 0),    # No step
}

# Type hints
Point = tuple[int, int]


def parse_line(line: str):
    return line.strip().split(" ")


def move(current_pos: Point, direction: str):
    step_mapping = STEP_VECTORS[direction]
    return add_points(current_pos, step_mapping)


def add_points(p_a: Point, p_b: Point):
    return p_a[0] + p_b[0], p_a[1] + p_b[1]


def single_step_towards_position(current_position: Point,
                                 target_position: Point):
    appropriate_step = (
        max(-1, min(1, target_position[0] - current_position[0])),
        max(-1, min(1, target_position[1] - current_position[1])),
    )
    return add_points(current_position, appropriate_step)


def positions_adjacent(pos_a: Point, pos_b: Point):
    for direction in STEP_VECTORS.keys():
        if pos_b == move(pos_a, direction):
            return True
    return False


def print_registered_steps(steps: Iterable):
    x_steps = [s[0] for s in steps]
    y_steps = [s[1] for s in steps]
    width = max(x_steps) - min(x_steps)
    height = max(y_steps) - min(y_steps)
    width_offset = min(x_steps)
    height_offset = min(y_steps)
    grid = [["." for _ in range(width)] for _ in range(height)]

    for step in steps:
        grid[step[0]+height_offset][step[1]+width_offset] = "#"
    for row in grid:
        print("".join(row))


def part_1():
    registered_steps = {}
    lines = open("day_09/input.txt").readlines()
    head_position = (0, 0)
    tail_position = (0, 0)
    registered_steps[tail_position] = 1
    for line in lines:
        direction, steps = parse_line(line)
        for _ in range(int(steps)):
            head_position = move(head_position, direction)
            if not positions_adjacent(head_position, tail_position):
                tail_position = single_step_towards_position(tail_position,
                                                             head_position)
                registered_steps[tail_position] = 1

    print("Part 1 - The number of different positions the tail has been in is "
          f"{len(registered_steps)}")


def part_2():
    registered_steps = {}
    lines = open("day_09/input.txt").readlines()
    knots = [(0, 0)]*10
    registered_steps[knots[-1]] = 1
    for line in lines:
        direction, steps = parse_line(line)
        for _ in range(int(steps)):
            knots[0] = move(knots[0], direction)
            for i in range(1, len(knots)):
                if not positions_adjacent(knots[i-1], knots[i]):
                    knots[i] = single_step_towards_position(knots[i],
                                                            knots[i-1])
            registered_steps[knots[-1]] = 1

    print("Part 2 - The number of different positions the tail has been in is "
          f"{len(registered_steps)}")


def main():
    part_1()
    part_2()


if __name__ == "__main__":
    main()
