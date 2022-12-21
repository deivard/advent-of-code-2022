"""Day 18: Boiling Boulders
"""

import matplotlib.pyplot as plt
import numpy as np

SIDES_MAP = [
    (1,  0,  0),
    (0,  1,  0),
    (0,  0,  1),
    (-1, 0,  0),
    (0, -1,  0),
    (0,  0, -1),
]


def find_cube_maxmin(cubes):
    positions = []
    for cube in cubes.keys():
        position = list(map(int, cube.split(",")))
        positions.append(position)

    x_max = max(positions, key=lambda p: p[0])[0]
    y_max = max(positions, key=lambda p: p[1])[1]
    z_max = max(positions, key=lambda p: p[2])[2]
    x_min = min(positions, key=lambda p: p[0])[0]
    y_min = min(positions, key=lambda p: p[1])[1]
    z_min = min(positions, key=lambda p: p[2])[2]

    return ((x_max, y_max, z_max), (x_min, y_min, z_min))


def create_bounding_air_cubes(cubes):
    maxes, mins = find_cube_maxmin(cubes)
    air_cubes = {}
    for x in range(mins[0]-1, maxes[0]+2):
        for y in range(mins[1]-1, maxes[1]+2):
            for z in range(mins[2]-1, maxes[2]+2):
                proposed_position = f"{x},{y},{z}"
                cube_in_position = cubes.get(proposed_position, None)
                if cube_in_position is None:
                    air_cubes[proposed_position] = 0
    return air_cubes


def get_adjacent_cubes(cube, cubes):
    adjacent_cubes = []
    for side in SIDES_MAP:
        position = list(map(int, cube.split(",")))
        position_to_check = [str(position[0] + side[0]),
                             str(position[1] + side[1]),
                             str(position[2] + side[2])]
        position_to_check = ",".join(position_to_check)
        adjacent_cube = cubes.get(position_to_check, None)

        if adjacent_cube is not None:
            adjacent_cubes.append(position_to_check)

    return adjacent_cubes


def group_cubes_into_blobs(cubes):
    blobs = []
    cubes_to_check = list(cubes.keys())
    while len(cubes_to_check):
        blob_open = [cubes_to_check.pop()]
        blob_closed = []
        while len(blob_open):
            current_cube = blob_open.pop()
            blob_closed.append(current_cube)
            adjacent_cubes = get_adjacent_cubes(current_cube, cubes)
            for adjacent_cube in adjacent_cubes:
                if adjacent_cube in cubes_to_check:
                    cubes_to_check.remove(adjacent_cube)
                if adjacent_cube not in blob_closed:
                    blob_open.append(adjacent_cube)
        blobs.append(blob_closed)
    return blobs


def blob_is_exposed(blob, cubes):
    maxes, mins = find_cube_maxmin(cubes)
    for point in blob:
        point = list(map(int, point.split(",")))
        if (maxes[0] <= point[0] or point[0] <= mins[0]
                or maxes[1] <= point[1] or point[1] <= mins[1]
                or maxes[2] <= point[2] or point[2] <= mins[2]):
            return True
    return False


def parse_input(filename: str):
    lines = {line.strip(): 6 for line in open(filename).readlines()}
    return lines


def update_sides_connected(cubes):
    for cube_position_str in cubes.keys():
        cubes_connected = []
        for side in SIDES_MAP:
            position = list(map(int, cube_position_str.split(",")))
            position_to_check = [str(position[0] + side[0]),
                                 str(position[1] + side[1]),
                                 str(position[2] + side[2])]
            position_to_check = ",".join(position_to_check)
            adjacent_cube = cubes.get(position_to_check, None)
            if adjacent_cube is not None:
                cubes_connected.append(position_to_check)
        cubes[cube_position_str] = (cubes[cube_position_str]
                                    - len(cubes_connected))


def get_surface_area(cubes):
    return sum(cubes.values())


def air_cube_sides_touching_cubes(air_cubes, cubes):
    for air_cube in air_cubes.keys():
        cubes_connected = []
        for side in SIDES_MAP:
            position = list(map(int, air_cube.split(",")))
            position_to_check = [str(position[0] + side[0]),
                                 str(position[1] + side[1]),
                                 str(position[2] + side[2])]
            position_to_check = ",".join(position_to_check)
            adjacent_cube = cubes.get(position_to_check, None)
            if adjacent_cube is not None:
                cubes_connected.append(position_to_check)
        air_cubes[air_cube] = len(cubes_connected)

    return sum([sides_connected_to_cubes
                for sides_connected_to_cubes in air_cubes.values()])


def plot_cubes(air_cubes, lava_cubes):
    cube_maxes, _ = find_cube_maxmin(lava_cubes)
    cube_points = np.array([list(map(int, cube.split(",")))
                            for cube in lava_cubes])
    air_cube_points = np.array([list(map(int, cube.split(",")))
                                for cube in air_cubes])

    combined_cube_voxel_positions = np.zeros(shape=(np.array(cube_maxes)+1))
    combined_colors = np.empty(combined_cube_voxel_positions.shape,
                               dtype=object)

    air_cube_voxel_positions = np.zeros(shape=(np.array(cube_maxes)+1))
    air_colors = np.empty(air_cube_voxel_positions.shape, dtype=object)
    for point in air_cube_points:
        combined_cube_voxel_positions[point[0]][point[1]][point[2]] = 1
        air_cube_voxel_positions[point[0]][point[1]][point[2]] = 1
        air_colors[point[0]][point[1]][point[2]] = "#6aa2e74D"
        combined_colors[point[0]][point[1]][point[2]] = "#6aa2e74D"

    lava_cube_voxel_positions = np.zeros(shape=(np.array(cube_maxes)+1))
    lava_colors = np.empty(lava_cube_voxel_positions.shape, dtype=object)
    for point in cube_points:
        combined_cube_voxel_positions[point[0]][point[1]][point[2]] = 1
        lava_cube_voxel_positions[point[0]][point[1]][point[2]] = 1
        lava_colors[point[0]][point[1]][point[2]] = "#dd2c2c4d"
        combined_colors[point[0]][point[1]][point[2]] = "#dd2c2c4d"

    # NOTE: This part is kind of broken :)
    fig = plt.figure()
    combined = fig.add_subplot(projection="3d")
    air = fig.add_subplot(projection="3d")
    lava = fig.add_subplot(projection="3d")
    air.voxels(air_cube_voxel_positions, facecolors=air_colors)
    air.set_aspect("auto")
    lava.voxels(lava_cube_voxel_positions, facecolors=lava_colors)
    lava.set_aspect("auto")
    combined.voxels(combined_cube_voxel_positions, facecolors=combined_colors)
    combined.set_aspect("auto")

    plt.show()


def part_1():
    cubes = parse_input("day_18/input.txt")
    update_sides_connected(cubes)
    surface_area = get_surface_area(cubes)
    print("Part 1 - Surface area of lava droplet is "
          f"{surface_area}")


def part_2():
    lava_cubes = parse_input("day_18/input.txt")
    update_sides_connected(lava_cubes)
    surface_area_cubes = get_surface_area(lava_cubes)
    air_cubes = create_bounding_air_cubes(lava_cubes)
    blobs = group_cubes_into_blobs(air_cubes)
    non_exposed_blobs = [blob for blob in blobs
                         if not blob_is_exposed(blob, lava_cubes)]
    flattened = []
    non_exposed_air_cubes = {}
    for c in non_exposed_blobs:
        flattened.extend(c)
    for c in flattened:
        non_exposed_air_cubes[c] = 0
    area_to_remove = air_cube_sides_touching_cubes(non_exposed_air_cubes,
                                                   lava_cubes)

    plot_cubes(non_exposed_air_cubes, lava_cubes)

    print("Part 2 - Exposed surface area of lava droplet is "
          f"{surface_area_cubes - area_to_remove}")


def main():
    part_1()
    part_2()


if __name__ == "__main__":
    main()
