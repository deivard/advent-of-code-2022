"""Day 12: Hill Climbing Algorithm
"""


from typing import Optional


def parse_file(filename: str) -> list[str]:
    return [list(line.strip()) for line in open(filename)]


def find_endpoints(grid: list[str]):
    start = None
    end = None
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if c == "S":
                start = (i, j)
            elif c == "E":
                end = (i, j)
    return start, end


def get_neighbouring_points(current_pos, grid):
    addends = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    valid_neighbours = set()
    for addend in addends:
        valid_neighbours.add(
            (min(len(grid)-1, max(0, current_pos[0] + addend[0])),
             min(len(grid[0])-1, max(0, current_pos[1] + addend[1])))
        )
    if current_pos in valid_neighbours:
        valid_neighbours.remove(current_pos)
    return valid_neighbours


def can_step_to_point(current, target, grid):
    current_elevation = grid[current[0]][current[1]]
    if current_elevation == "S":
        current_elevation = "a"
    target_elevation = grid[target[0]][target[1]]
    if target_elevation == "E":
        target_elevation = "z"
    return ord(target_elevation) - ord(current_elevation) <= 1


def can_step_to_end(current_pos, grid):
    neighbours = get_neighbouring_points(current_pos, grid)
    for point in neighbours:
        if (grid[point[0]][point[1]] == "E" and
                can_step_to_point(current_pos, point, grid)):
            return True

    return False


def get_steppable_steps(current_pos: tuple[int, int], grid: list[str]):
    row, column = current_pos
    current_elevation = grid[row][column]
    if current_elevation == "S":
        current_elevation = "a"
    neighbours = get_neighbouring_points(current_pos, grid)

    return [
        point for point in neighbours
        if can_step_to_point(current_pos, point, grid)
        # if (ord(grid[point[0]][point[1]]) - ord("a") - ord(current_elevation)) <= 1
    ]


class Node:
    def __init__(self, position, parent=None) -> None:
        self.parent = parent
        self.position = position

        self.f = 0
        self.g = 0
        self.h = 0

    def __eq__(self, other):
        return self.position == other.position

def remove_visited_steps(steps, visited):
    for point in visited:
        if point in steps:
            steps.remove(point)
    return steps


def create_tree(position, grid, parent):
    # current_node = root
    root = Node(
        position,
        parent.visited + [position] if parent is not None else []
    )
    if can_step_to_end(position, grid):
        root.can_step_to_end = True
        return root
    steppable_steps = get_steppable_steps(position, grid)
    steppable_steps = remove_visited_steps(steppable_steps, root.visited)
    root.children = [create_tree(step, grid, root) for step in steppable_steps]
    # print("".join([grid[point[0]][point[1]] for point in root.visited]))
    return root


def calculate_path_lengths(root, accumulator):
    if root.can_step_to_end:
        accumulator.append(root.visited)
    else:
        for child in root.children:
            (calculate_path_lengths(child, accumulator))


def find_best_candidate_node_index(open_list: list[Node]):
    best = open_list[0]
    index = 0
    for i, node in enumerate(open_list):
        if node.f < best.f:
            index = i
            best = node
            
    return index


def distance_heuristic(current_pos, goal_pos):
    # Manhattan distance
    return abs(current_pos[0]-goal_pos[0]) + abs(current_pos[1]-goal_pos[1])


def find_shortest_path(start_point, end_point, grid):
    start_node = Node(start_point)
    end_node = Node(end_point)
    open_list = [start_node]
    closed_list = []

    while len(open_list):
        best_index = find_best_candidate_node_index(open_list)
        current_node = open_list.pop(best_index)
        closed_list.append(current_node)
        
        if current_node == end_node:
            break
        
        position_candidates = get_steppable_steps(current_node.position, grid)
        candidate_nodes = [Node(pos, current_node)
                           for pos in position_candidates]
        
        for node in candidate_nodes:
            if node in closed_list:
                continue
            node.g = current_node.g + 1
            node.h = distance_heuristic(node.position, end_node.position)
            node.f = node.g + node.h
            if node not in open_list:
                # node.g = current_node.g + 1
                # node.h = distance_heuristic(node.position, end_node.position)
                # node.f = node.g + node.h
                open_list.append(node)
            else:
                index_of_duplicate = open_list.index(node)
                if open_list[index_of_duplicate].g >= node.g:
                    open_list[index_of_duplicate] = node
                    # open_list[index_of_duplicate].parent = current_node
                    # open_list[index_of_duplicate].g = current_node.g + 1
                    # open_list[index_of_duplicate].h = distance_heuristic(
                    #     open_list[index_of_duplicate].position, end_node.position
                    # )
                    # open_list[index_of_duplicate].f = (open_list[index_of_duplicate].g + open_list[index_of_duplicate].h)
    path = []
    while current_node.parent is not None:
        path.append(current_node.position)
        current_node = current_node.parent
        
    return path


def is_next_to_b(point, grid):
    neighbours = get_neighbouring_points(point, grid)
    for p in neighbours:
        if grid[p[0]][p[1]] == "b":
            return True
    return False


def find_possible_starting_points(grid):
    starting_points = []
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if c in "Sa":
                if is_next_to_b((i, j), grid):
                    starting_points.append((i, j))

    return starting_points


def print_path(path, grid):
    for point in path:
        grid[point[0]][point[1]] = f"\033[0;31m{grid[point[0]][point[1]]}\033[0m"
    for row in grid:
        print("".join(row))


def part_1():
    grid = parse_file("day_12/input.txt")
    starting_point, end_point = find_endpoints(grid)
    shortest_path = find_shortest_path(starting_point, end_point, grid)
    print(len(shortest_path))
    print_path(shortest_path, grid)


def part_2():
    grid = parse_file("day_12/input.txt")
    _, end_point = find_endpoints(grid)
    starting_points = find_possible_starting_points(grid)
    possible_paths = []
    for starting_point in starting_points:
        possible_paths.append(find_shortest_path(starting_point, end_point, grid))
    
    path_lens = [len(path) for path in possible_paths]
    print(min(path_lens))
    # print(min(map(len, possible_paths)))



def main():
    # part_1()
    part_2()


if __name__ == "__main__":
    main()
