"""Day 14: Regolith Reservoir
"""


import os
import time


def get_rock_paths_from_lines(lines: list[str]):
    paths = []
    for line in lines:
        unparsed_points = line.strip().replace(" ", "").split("->")
        points = [tuple(map(int, up.split(","))) for up in unparsed_points]
        paths.append(points)
    return paths


def find_min_max(iterable):
    return min(iterable), max(iterable)


def find_map_boundaries(rock_paths: list[tuple[int, int]]):
    x_indices = []
    y_indices = []
    for path in rock_paths:
        for point in path:
            x_indices.append(point[0])
            y_indices.append(point[1])
    x_min, x_max = find_min_max(x_indices)
    y_min, y_max = find_min_max(y_indices)

    return (x_min, y_min), (x_max, y_max)


def find_sand_boundaries(cave_map):
    x_max = y_max = 0
    x_min = y_min = 2**64
    for y in range(len(cave_map)):
        for x in range(len(cave_map[0])):
            if cave_map[y][x] == "o":
                x_max = max(x, x_max)
                y_max = max(y, y_max)
                x_min = min(x, x_min)
                y_min = min(y, y_min)

    return ((max(0, x_min-1), max(0, y_min-1)),
            (min(x_max+1, len(cave_map[0])), min(y_max+1, len(cave_map))))


def create_empty_map_from_max_boundary(max_boundary: tuple[int, int]):
    return [["." for _ in range(max_boundary[0]+1)]
            for _ in range(max_boundary[1]+1)]


def auto_crop_map(cave_map, boundaries):
    x_min = boundaries[0][0]
    x_max = boundaries[1][0]+1
    y_min = boundaries[0][1]
    y_max = boundaries[1][1]+1

    cropped_map = []
    for row in cave_map[y_min:y_max]:
        cropped_map.append(row[x_min:x_max])

    return cropped_map


def place_rock_paths_on_map(paths: list[list[tuple[int, int]]],
                            cave_map: list[list[str]]):
    for path in paths:
        for i in range(len(path)-1):
            x_start = min((path[i+1][0], path[i][0]))-1
            x_end = max((path[i+1][0], path[i][0]))

            y_start = min((path[i+1][1], path[i][1]))-1
            y_end = max((path[i+1][1], path[i][1]))

            for x in range(x_start, x_end):
                for y in range(y_start, y_end):
                    cave_map[y+1][x+1] = "#"

    return cave_map


def print_map(cave_map: list[list[str]], boundaries=None):
    if boundaries is not None:
        x_min = boundaries[0][0]
        x_max = boundaries[1][0]
        y_min = boundaries[0][1]
        y_max = boundaries[1][1]
    else:
        x_min = 0
        x_max = len(cave_map[0])-1
        y_min = 0
        y_max = len(cave_map)-1

    map_str = ""
    line_rows = 2
    print()  # Empty row
    print(f"{' '.rjust(3)} "
          + str(x_min) + " "
          + str(x_max).rjust((x_max-x_min) - len(str(x_max))))
    for y in range(y_min, y_max+1):
        map_str += (f"{str(y).rjust(3)} " + "".join(cave_map[y][x_min:x_max+1])
                    .replace("o", "\033[0;93mo\033[0m")
                    .replace("#", "\033[0;30m#\033[0m")
                    .replace(".", "\033[0;94m.\033[0m")
                    + "\n")
        line_rows += 1
    print(map_str)
    return line_rows


def find_sand_landing_position(cave_map, sand_index=(0, 500)):
    max_row = len(cave_map)-1
    y, x = sand_index
    if y+1 > max_row or (0 > x >= len(cave_map[0])):
        raise ValueError("Sand flowed to the abyss")
    elif cave_map[y+1][x] == ".":
        position = find_sand_landing_position(cave_map, (y+1, x))
    else:
        # Left down
        if cave_map[y+1][x-1] == ".":
            position = find_sand_landing_position(cave_map, (y+1, x-1))
        # Right down
        elif cave_map[y+1][x+1] == ".":
            position = find_sand_landing_position(cave_map, (y+1, x+1))
        # Settled
        else:
            position = (y, x)

    return position


def increase_map_width(cave_map, side_increase_amount=10):
    for _ in range(side_increase_amount):
        for row in cave_map[:-1]:
            row.insert(0, ".")
            row.append(".")
        cave_map[-1].insert(0, "#")
        cave_map[-1].append("#")

    return cave_map


def find_point_before_collision(pos, cave_map):
    x = pos[1]
    for y in range(pos[0], len(cave_map)-1):
        if cave_map[y+1][x] != ".":
            return y, x
    raise ValueError("No downward collison found.")


def find_sand_landing_position_infinite_floor(cave_map,
                                              x_offset=0,
                                              sand_index=(0, 500)):
    map_width = len(cave_map[0])
    y, x = sand_index
    map_width_increment = 10
    if x >= map_width-2 or x < 1:
        cave_map = increase_map_width(cave_map, map_width_increment)
        x_offset += map_width_increment
        x += map_width_increment

    if cave_map[y+1][x] == ".":
        collision_point = find_point_before_collision((y, x), cave_map)
        position, x_offset = find_sand_landing_position_infinite_floor(
            cave_map, x_offset, collision_point
        )
    else:
        # Left down
        if cave_map[y+1][x-1] == ".":
            position, x_offset = find_sand_landing_position_infinite_floor(
                cave_map, x_offset, (y+1, x-1)
            )
        # Right down
        elif cave_map[y+1][x+1] == ".":
            position, x_offset = find_sand_landing_position_infinite_floor(
                cave_map, x_offset, (y+1, x+1)
            )
        # Settled
        else:
            position = (y, x)

    return position, x_offset


def visualization_demo():
    os.system("cls")
    input("Maximize your terminal and press enter to start...")

    lines = open("day_14/demo_input.txt").readlines()
    rock_paths = get_rock_paths_from_lines(lines)
    _, max_boundaries = find_map_boundaries(rock_paths)
    max_boundaries = max_boundaries[0], max_boundaries[1] + 2
    cave_map = create_empty_map_from_max_boundary(max_boundaries)
    cave_map = place_rock_paths_on_map(rock_paths, cave_map)
    # Remove part of the map so it fits the terminal
    cave_map = cave_map[5:5+os.get_terminal_size().lines-4]
    cave_map[-1] = ["#" for _ in range(len(cave_map[-1]))]

    sand_start_pos = (0, 500)
    start_offset = 0
    num_sand_settled = 0
    printed_rows = 0
    sleep_time = 0.05
    min_sleep_time = 0
    while cave_map[sand_start_pos[0]][sand_start_pos[1]] != "o":
        sand_start_pos = (0, 500+start_offset)
        sand_pos, start_offset = find_sand_landing_position_infinite_floor(
            cave_map, start_offset, sand_index=sand_start_pos
        )
        cave_map[sand_pos[0]][sand_pos[1]] = "o"
        num_sand_settled += 1

        sand_boundaries = find_sand_boundaries(cave_map)
        printed_rows = print_map(cave_map, sand_boundaries)
        print("\033[F"*(printed_rows+2), end="")
        time.sleep(sleep_time)
        sleep_time = max(sleep_time*0.99, min_sleep_time)

    sand_boundaries = find_sand_boundaries(cave_map)
    print_map(cave_map, sand_boundaries)
    print(f"Part 2 - Sand reached the top after {num_sand_settled}"
          " sand units had settled.")


def part_1():
    lines = open("day_14/input.txt").readlines()
    rock_paths = get_rock_paths_from_lines(lines)
    min_boundaries, max_boundaries = find_map_boundaries(rock_paths)
    cave_map = create_empty_map_from_max_boundary(max_boundaries)
    cave_map = place_rock_paths_on_map(rock_paths, cave_map)

    num_sand_settled = 0
    while True:
        try:
            sand_position = find_sand_landing_position(cave_map, (0, 500))
            cave_map[sand_position[0]][sand_position[1]] = "o"
            num_sand_settled += 1
        except ValueError:
            break

    print_map(cave_map, ((min_boundaries[0], 0), max_boundaries))
    print(f"Part 1 - Sand flowed into the abyss after {num_sand_settled}"
          " sand units had settled.")


def part_2():
    lines = open("day_14/input.txt").readlines()
    rock_paths = get_rock_paths_from_lines(lines)
    _, max_boundaries = find_map_boundaries(rock_paths)
    max_boundaries = max_boundaries[0], max_boundaries[1] + 2
    cave_map = create_empty_map_from_max_boundary(max_boundaries)
    cave_map = place_rock_paths_on_map(rock_paths, cave_map)
    cave_map[-1] = ["#" for _ in range(len(cave_map[-1]))]

    sand_start_position = (0, 500)
    start_offset = 0
    num_sand_settled = 0
    while cave_map[sand_start_position[0]][sand_start_position[1]] != "o":
        sand_start_position = (0, 500+start_offset)
        sand_pos, start_offset = find_sand_landing_position_infinite_floor(
            cave_map, start_offset, sand_index=sand_start_position
        )
        cave_map[sand_pos[0]][sand_pos[1]] = "o"
        num_sand_settled += 1

    sand_boundaries = find_sand_boundaries(cave_map)
    print_map(cave_map, sand_boundaries)
    print(f"Part 2 - Sand reached the top after {num_sand_settled}"
          " sand units had settled.")


def main():
    # part_1()
    # part_2()
    visualization_demo()


if __name__ == "__main__":
    main()
