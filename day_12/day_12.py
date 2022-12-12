"""Day 12: Hill Climbing Algorithm
"""


class Node:
    def __init__(self, position, parent=None) -> None:
        self.parent = parent
        self.position = position

        self.f = 0
        self.g = 0
        self.h = 0

    def __eq__(self, other):
        return self.position == other.position


def parse_file(filename: str) -> list[str]:
    return [list(line.strip()) for line in open(filename)]


def find_endpoints(grid: list[list[str]]):
    start = None
    end = None
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            if c == "S":
                start = (i, j)
            elif c == "E":
                end = (i, j)
    return start, end


def get_neighbouring_points(current_pos: tuple[int, int],
                            grid: list[list[str]]):
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


def elevation_delta(point_a: tuple[int, int],
                    point_b: tuple[int, int],
                    grid: list[list[str]]):
    a_elevation = (grid[point_a[0]][point_a[1]]
                   .replace("S", "a")
                   .replace("E", "z"))
    b_elevation = (grid[point_b[0]][point_b[1]]
                   .replace("S", "a")
                   .replace("E", "z"))
    return ord(b_elevation) - ord(a_elevation)


def can_step_to_point(current: tuple[int, int],
                      target: tuple[int, int],
                      grid: list[list[str]]):
    return elevation_delta(current, target, grid) <= 1


def get_steppable_steps(current_pos: tuple[int, int],
                        grid: list[str]):
    neighbours = get_neighbouring_points(current_pos, grid)
    return [point for point in neighbours
            if can_step_to_point(current_pos, point, grid)]


def find_best_candidate_node_index(open_list: list[Node]):
    best = open_list[0]
    index = 0
    for i, node in enumerate(open_list):
        if node.f < best.f:
            index = i
            best = node

    return index


def distance_heuristic(current_pos: tuple[int, int],
                       goal_pos: tuple[int, int]):
    # Manhattan distance
    return abs(current_pos[0]-goal_pos[0]) + abs(current_pos[1]-goal_pos[1])


def get_path_to_node(node: Node):
    path = []
    current_node = node
    while current_node.parent is not None:
        path.append(current_node.position)
        current_node = current_node.parent

    return path[::-1]




def find_shortest_path_astar(start_point: tuple[int, int],
                             end_point: tuple[int, int],
                             grid: list[list[str]]) -> list[tuple[int, int]]:
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
            if node in open_list:
                index_of_duplicate = open_list.index(node)
                if open_list[index_of_duplicate].g >= node.g:
                    open_list[index_of_duplicate] = node
            else:
                open_list.append(node)

    return get_path_to_node(current_node)


def adjacent_to_char(point: tuple[int, int], char: str, grid: list[list[str]]):
    neighbours = get_neighbouring_points(point, grid)
    for p in neighbours:
        if grid[p[0]][p[1]] == char:
            return True
    return False


def find_possible_starting_points(grid: list[list[str]]):
    starting_points = []
    for i, row in enumerate(grid):
        for j, c in enumerate(row):
            # Check if the "a" point is adjacent to a B so it isnt stuck
            # or one of the suboptimal starting points.
            if c in "Sa" and adjacent_to_char((i, j), "b", grid):
                starting_points.append((i, j))

    return starting_points


def print_path(path: list[tuple[int, int]], grid: list[list[str]]):
    for point in path:
        grid[point[0]][point[1]] = f"\033[0;31m{grid[point[0]][point[1]]}\033[0m"
    for row in grid:
        print("".join(row))


def get_subpath_if_it_exists(point: tuple[int, int],
                             paths: list[list[tuple[int, int]]]):
    for path in paths:
        if point in path:
            return path[path.index(point):]
    return None


def part_1():
    grid = parse_file("day_12/input.txt")
    starting_point, end_point = find_endpoints(grid)
    shortest_path = find_shortest_path_astar(starting_point, end_point, grid)
    print(f"Part 1 - Length of the shortest path: {len(shortest_path)}")
    print_path(shortest_path, grid)


def part_2():
    """Comment about part 2: This approach is rather inefficient
    since many paths needs to be computed. A better approach would be to use
    Dijkstra's shortest path algorithm with the end position "E" as starting
    point and any position with elevation "a" as a valid end point. This would
    require a different "valid step condition" (delta elevation must be >= -1).
    In the end, I couldn't be arsed to implement Dijkstra's algorithm :)
    """
    grid = parse_file("day_12/input.txt")
    _, end_point = find_endpoints(grid)
    starting_points = find_possible_starting_points(grid)
    possible_paths = []
    for starting_point in starting_points:
        # Save some time by seeing if the subpath exists, which
        # it does if the starting point exists in another path
        path = get_subpath_if_it_exists(starting_point, possible_paths)
        if path is None:
            path = find_shortest_path_astar(starting_point, end_point, grid)
        possible_paths.append(path)

    path_lens = [len(path) for path in possible_paths]
    shortest_path = min(path_lens)
    print(f"Part 2 - Length of the shortest path: {shortest_path}")
    print_path(shortest_path, grid)


def main():
    part_1()
    part_2()


if __name__ == "__main__":
    main()
