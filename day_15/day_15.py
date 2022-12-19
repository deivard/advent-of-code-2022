"""Day 15: Beacon Exclusion Zone
"""


class Sensor:
    def __init__(self, position, closest_beacon) -> None:
        self.position = position
        self.closest_beacon = closest_beacon
        self.distance_to_beacon = manhattan_distance(
            self.position, self.closest_beacon
        )


def positions_from_line(line):
    line = line.strip().split(" ")
    sensor_x = int(line[2].split("=")[-1].replace(",", ""))
    sensor_y = int(line[3].split("=")[-1].replace(":", ""))
    beacon_x = int(line[8].split("=")[-1].replace(",", ""))
    beacon_y = int(line[9].split("=")[-1])

    return (sensor_x, sensor_y), (beacon_x, beacon_y)


def find_min_max(iterable):
    return min(iterable), max(iterable)


def manhattan_distance(point_a, point_b):
    return abs(point_a[0] - point_b[0]) + abs(point_a[1] - point_b[1])


def create_map_from_sensors(sensors):
    sensors_x = [sensor.position[0] for sensor in sensors]
    sensors_y = [sensor.position[1] for sensor in sensors]
    beacons_x = [sensor.closest_beacon[0] for sensor in sensors]
    beacons_y = [sensor.closest_beacon[1] for sensor in sensors]
    x_min, x_max = find_min_max(sensors_x + beacons_x)
    y_min, y_max = find_min_max(sensors_y + beacons_y)
    x_len = x_max - x_min
    y_len = y_max - y_min

    map_ = [["." for _ in range(x_len+1)] for _ in range(y_len+1)]
    x_offset = min(0, x_min)
    y_offset = min(0, y_min)
    for sensor in sensors:
        map_[sensor.position[1]-y_offset][sensor.position[0]-x_offset] = "S"
        map_[sensor.closest_beacon[1]-y_offset][sensor.closest_beacon[0]-x_offset] = "B"

    return map_


def get_bounding_circle(sensor):
    """Lord have mercy for I have taxicabbed.
    """
    top = sensor.position[0], sensor.position[1]+sensor.distance_to_beacon+1
    right = sensor.position[0]+sensor.distance_to_beacon+1, sensor.position[1]
    bottom = sensor.position[0], sensor.position[1]-sensor.distance_to_beacon-1
    left = sensor.position[0]-sensor.distance_to_beacon-1, sensor.position[1]

    directions = [
        (1, -1), # Top to right
        (-1, -1), # Right to bottom
        (-1, 1),  # Bottom to left
        (1, 1)  # left to top
    ]
    bounding_circle = []

    current_pos = top
    while current_pos != right:
        bounding_circle.append(current_pos)
        current_pos = current_pos[0] + directions[0][0], current_pos[1] + directions[0][1]

    current_pos = right
    while current_pos != bottom:
        bounding_circle.append(current_pos)
        current_pos = current_pos[0] + directions[1][0], current_pos[1] + directions[1][1]

    current_pos = bottom
    while current_pos != left:
        bounding_circle.append(current_pos)
        current_pos = current_pos[0] + directions[2][0], current_pos[1] + directions[2][1]

    current_pos = left
    while current_pos != top:
        bounding_circle.append(current_pos)
        current_pos = current_pos[0] + directions[3][0], current_pos[1] + directions[3][1]

    return bounding_circle


def part_1():
    lines = open("day_15/input.txt").readlines()
    sensors = []
    # y = 10
    y = 2000000
    for line in lines:
        sensor_pos, beacon_pos = positions_from_line(line)
        sensors.append(Sensor(sensor_pos, beacon_pos))

    invalid_positions = set()
    for sensor in sensors:
        # Create list of y values as wide as sensor distance x2
        start = sensor.position[0]-sensor.distance_to_beacon
        end = sensor.position[0]+sensor.distance_to_beacon
        values_to_check = [(x, y) for x in range(start, end)]
        # Check if sensor y is in range of y value
        distances_to_values = [
            (value_to_check, manhattan_distance(sensor.position, value_to_check))
            for value_to_check in values_to_check
        ]
        for i in list(filter(lambda d: d[1] <= sensor.distance_to_beacon,
                             distances_to_values)):
            invalid_positions.add(i[0])

        for sensor in sensors:
            if sensor.position in invalid_positions:
                invalid_positions.remove(sensor.position)
            if sensor.closest_beacon in invalid_positions:
                invalid_positions.remove(sensor.closest_beacon)

    print(f"Part 1 - Number of invalid positions: {len(invalid_positions)}")


def part_2():
    lines = open("day_15/input.txt").readlines()
    sensors = []
    for line in lines:
        sensor_pos, beacon_pos = positions_from_line(line)
        sensors.append(Sensor(sensor_pos, beacon_pos))

    possible_locations = set()
    finished_sensors = 0
    circles = []
    for sensor in sensors:
        circles.append(set(get_bounding_circle(sensor)))
        finished_sensors += 1

    for sensor in sensors:
        bounding_circle = get_bounding_circle(sensor)
        for p in bounding_circle:
            if 0 < p[0] <= 4_000_000 and 0 < p[1] <= 4_000_000:
                outrange_all_sensors = True
                for s in sensors:
                    if manhattan_distance(p, s.position) <= s.distance_to_beacon:
                        outrange_all_sensors = False
                        break
                if outrange_all_sensors:
                    possible_locations.add(p)
        finished_sensors += 1
        print(f"Finished sensor {finished_sensors} of {len(sensors)}")
    sensor_pos = possible_locations[0]
    tuning_freq = (sensor_pos[0]*4_000_000) + sensor_pos[1]
    print("Part 2 - The tuning frequency for the missing sensor "
          f"is {tuning_freq}")


def main():
    part_1()
    part_2()


if __name__ == "__main__":
    main()
