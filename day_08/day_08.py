"""Day 8: Treetop Tree House
"""
from math import prod
from typing import Iterable


def trees_visible_in_line(tree_line: Iterable):
    tallest_tree = -1
    visible_trees_mask = [0] * len(tree_line)
    for i, tree_height in enumerate(tree_line):
        if int(tree_height) > int(tallest_tree):
            tallest_tree = tree_height
            visible_trees_mask[i] = 1

    return visible_trees_mask


def merge_visibility_masks(visibility_masks: tuple[Iterable[int], Iterable[int]]):
    return [int(bool(sum(pair))) for pair in
            zip(visibility_masks[0], visibility_masks[1])]


def visibility_mask_to_indices(visibility_mask: Iterable[int]):
    return [i for i in range(len(visibility_mask)) if visibility_mask[i] != 0]


def record_visible_trees_in_dict(coordinates: tuple[int, int],
                                 visible_trees_record: dict):
    for coordinate in coordinates:
        visible_trees_record[coordinate] = 1

    return visible_trees_record


def calculate_view_distance(view_height: int, trees_in_sight_line: Iterable):
    view_distance = 0
    for tree_height in trees_in_sight_line:
        view_distance += 1
        if int(tree_height) >= int(view_height):
            break
    return view_distance


def calculate_view_distances(view_height: int,
                             tree_sight_lines: Iterable[Iterable]):
    return [calculate_view_distance(view_height, sight_line)
            for sight_line in tree_sight_lines]


def calculate_tree_scenic_score(tree_position: Iterable[int, int],
                                grid: Iterable[Iterable]):
    trees_to_the_left = grid[tree_position[0]][:tree_position[1]][::-1]
    trees_to_the_right = grid[tree_position[0]][tree_position[1]+1:]
    trees_up = [
        grid[row_index][tree_position[1]]
        for row_index in range(tree_position[0]-1, -1, -1)
    ]
    trees_down = [
        grid[row_index][tree_position[1]]
        for row_index in range(tree_position[0]+1, len(grid[0]))
    ]
    view_height = grid[tree_position[0]][tree_position[1]]
    view_distances = calculate_view_distances(
        view_height,
        [trees_to_the_left, trees_to_the_right, trees_up, trees_down]
    )

    return prod(view_distances)


def calculate_scenic_scores(grid: Iterable[Iterable]):
    scenic_scores = []
    for row_index in range(0, len(grid)):
        for column_index in range(0, len(grid[0])):
            scenic_scores.append(
                calculate_tree_scenic_score(
                    [row_index, column_index],
                    grid
                )
            )
    return scenic_scores


def part_1():
    grid = list(map(str.strip, open("day_08/input.txt").readlines()))
    visible_trees_record = {}

    # Left and right
    for row_index in range(0, len(grid)):
        row = grid[row_index]
        from_left = trees_visible_in_line(row)
        from_right = trees_visible_in_line(row[::-1])
        merged_masks = merge_visibility_masks((from_left, from_right[::-1]))
        indices = visibility_mask_to_indices(merged_masks)
        coordinates = zip([row_index]*len(indices), indices)
        record_visible_trees_in_dict(coordinates, visible_trees_record)

    # Top and bottom
    for column_index in range(0, len(grid[0])):
        column = "".join([row[column_index] for row in grid])
        from_top = trees_visible_in_line(column)
        from_bottom = trees_visible_in_line(column[::-1])
        merged_masks = merge_visibility_masks((from_top, from_bottom[::-1]))
        indices = visibility_mask_to_indices(merged_masks)
        coordinates = zip(indices, [column_index]*len(indices))
        record_visible_trees_in_dict(coordinates, visible_trees_record)

    print("Part 1 - Number of trees visible from the edges: "
          f"{len(visible_trees_record)}")


def part_2():
    grid = list(map(str.strip, open("day_08/input.txt").readlines()))
    scenic_scores = calculate_scenic_scores(grid)

    print("Part 2 - The highest scenic score for any tree is "
          f"{max(scenic_scores)}")


def main():
    part_1()
    part_2()


if __name__ == "__main__":
    main()
