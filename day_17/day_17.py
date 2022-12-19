"""Day 17: Pyroclastic Flow
"""


from copy import deepcopy


def parse_blocks_file(filename: str):
    blocks = open(filename).read().split("\n\n")
    list_blocks = []
    for block in blocks:
        list_block = []
        for line in block.split("\n"):
            list_block.append(list(line))
        list_blocks.append(list_block)

    return list_blocks


class Shape:
    def __init__(self, line_block) -> None:
        self.shape_map = self.create_shape_map_from_line_block(line_block)
        self.height = len(line_block)
        self.points_in_chamber = None
        # self.position_in_chamber = None

    def move(self, direction):
        if self.points_in_chamber is None:
            raise ValueError("Shape is not yet placed in the chamber.")
        # print("asd")
        dir_map = {
            "<": (0, -1),
            ">": (0, 1),
            "down": (-1, 0)
        }
        self.points_in_chamber = [(point[0] + dir_map[direction][0],
                                  point[1] + dir_map[direction][1])
                                  for point in self.points_in_chamber]

    def get_points_in_chamber(self):
        return self.points_in_chamber
        return [
            (point[0] + self.points_in_chamber[0],
             point[1] + self.points_in_chamber[1])
            for point in self.shape_map
        ]

    def create_shape_map_from_line_block(self, line_block):
        shape_map = []
        for y, row in enumerate(line_block):
            for x, character in enumerate(row):
                if character != ".":
                    shape_map.append((y, x))
        return shape_map

    
class Chamber:
    def __init__(self, width: int = 7) -> None:
        self.shapes_present = []
        self.width = width
        self.__chamber = []
        self.current_highest = 0
        self.__prev_current_highest = 0
        self.current_highest_increment = 0

    def height(self):
        return len(self.__chamber)

    def raster_shape(self, shape: Shape):
        for point in shape.points_in_chamber:
            self.__chamber[point[0]][point[1]] = "#"
    
    def get_fingerprint(self, block_index, jet_index):
        lowest_blocker = self.current_highest
        for x in range(self.width):
            y = self.current_highest
            while self.__chamber[y][x] == "." and y > 0:
                y -= 1
            if y < lowest_blocker:
                lowest_blocker = y
            
        tower_chunk = self.__chamber[lowest_blocker:self.current_highest]
        fingerprint = "".join(["".join(row) for row in tower_chunk])
        fingerprint += f"_block_index_{block_index}_jet_index_{jet_index}"
        return fingerprint
    
    def point_is_occupied(self, point):
        return self.__chamber[point[0]][point[1]] == "#"
    # def crop_chamber(self):
    #     indices_blocked = [0]*self.width
    #     prefered_crop_point = 0
    #     chamber = self.__render_shapes()
    #     for row in chamber[::-1]:
    #         for character in row:
    
    def __chamber_is_high_enough(self, shape):
        return self.current_highest + 3 + shape.height < len(self.__chamber)
    
    def __make_chamber_fit_shape(self, shape: Shape):
        increment_amount = (3 + self.current_highest + shape.height) - self.height()
                            
        increment = [["." for _ in range(self.width)]
                     for _ in range(increment_amount)]
        self.__chamber.extend(increment)

    
    def update_current_highest(self, shape: Shape):
        self.__prev_current_highest = self.current_highest
        for point in shape.points_in_chamber:
            if point[0]+1 > self.current_highest:
                self.current_highest = point[0]+1
        self.current_highest_increment = self.current_highest - self.__prev_current_highest

        
        # for shape in self.shapes_present:
        #     for point in shape.points_in_chamber:
        #         if point[0]+1 > self.current_highest:
        #             self.current_highest = point[0]+1
    
    def loop_exists(self):
        # self.__chamber = [
        #     [".", ".", ".", ".", "#", "#", "."],
        #     [".", ".", ".", ".", "#", "#", "."],
        #     [".", ".", ".", ".", "#", ".", "."],
        #     [".", ".", "#", ".", "#", ".", "."],
        #     [".", ".", "#", ".", "#", ".", "."],
        #     ["#", "#", "#", "#", "#", ".", "."],
        #     [".", ".", "#", "#", "#", ".", "."],
        #     [".", ".", ".", "#", ".", ".", "."],
        #     [".", ".", "#", "#", "#", "#", "."],
        #     [".", ".", ".", ".", "#", "#", "."],
        #     [".", ".", ".", ".", "#", "#", "."],
        #     [".", ".", ".", ".", "#", ".", "."],
        #     [".", ".", "#", ".", "#", ".", "."],
        #     [".", ".", "#", ".", "#", ".", "."],
        #     ["#", "#", "#", "#", "#", ".", "."],
        #     [".", ".", "#", "#", "#", ".", "."],
        #     [".", ".", ".", "#", ".", ".", "."],
        #     [".", ".", "#", "#", "#", "#", "."],
        # ]

        mid_point = self.current_highest // 2
        top = self.__chamber[mid_point:self.current_highest]
        bottom = self.__chamber[:mid_point]
        # print("------")
        # for t, b in zip(top, bottom):
        #     print(f"{''.join(t)}     {''.join(b)}")
        if len(top) == len(bottom):
            for t, b in zip(top, bottom):
                if t != b:
                    return False
            return True
        return False

    def add_shape_to_chamber(self, shape: Shape):
        if not self.__chamber_is_high_enough(shape):
            self.__make_chamber_fit_shape(shape)
        shape.points_in_chamber = [
            # [self.height() - 1 - point[0], point[1] + 2]
            [self.current_highest + 3 + shape.height - 1 - point[0], point[1] + 2]
            for point in shape.shape_map
        ]
        # shape.points_in_chamber = (0, 2)
        self.shapes_present.append(shape)

    def __render_shapes(self):
        chamber = deepcopy(self.__chamber)
        for shape in self.shapes_present:
            for point in shape.points_in_chamber:
                # offset = shape.position_offset
                # y = point[0] + offset[0]
                # x = point[1] + offset[1]
                chamber[point[0]][point[1]] = "#"
        return chamber
        

    # def __repr__(self) -> str:
    #     return self.__str__()

    def __str__(self) -> str:
        chamber_with_shapes = self.__render_shapes()
        string = ""
        for row in chamber_with_shapes[::-1]:
            string += "|" + "".join(row) + "|\n"
        string += f"+{'-'*len(chamber_with_shapes[0])}+"
        return string


def next_position_points(direction: str, shape: Shape):
    dir_map = {
        "<": (0, -1),
        ">": (0, 1),
        "down": (-1, 0),  # 1 down from top
    }
    return [(point[0] + dir_map[direction][0],
            point[1] + dir_map[direction][1])
            for point in shape.points_in_chamber]


def points_obstructed(points_a, points_b):
    for point in points_a:
        if point in points_b:
            return True
    return False
    # for shape_in_chamber in chamber.shapes_present:
    #     if shape_in_chamber == shape:
    #         continue
    #     if point in shape_in_chamber.get_positions_in_chamber():
    #         return False


def points_obstructed(points, chamber: Chamber):
    for point in points:
        if chamber.point_is_occupied(point):
            return True
    return False


def shape_can_move_in_direction(direction: str, shape: Shape,
                                chamber: Chamber):
    # TODO: DOnt check all points
    next_points = next_position_points(direction, shape)
    for point in next_points:
        if not (0 <= point[1] < chamber.width):
            return False
    if points_obstructed(next_points, chamber):
        return False
    return True


def shape_can_fall(shape: Shape, chamber: Chamber):
    next_points = next_position_points("down", shape)

    for point in next_points:
        if point[0] < 0:
            return False
    if points_obstructed(next_points, chamber):
        return False
    return True


def part_1():
    blocks = parse_blocks_file("day_17/blocks.txt")
    jet_pattern = open("day_17/input.txt").read().strip()
    chamber = Chamber()
    current_shape = Shape(blocks[0])
    block_index = 0
    rock_settled = False
    chamber.add_shape_to_chamber(current_shape)
    jet_index = 0
    jet_direction = jet_pattern[0]
    rocks_settled = 0
    rocks_to_settle = 2022
    while rocks_settled < rocks_to_settle:
        # print(chamber)
        if shape_can_move_in_direction(jet_direction, current_shape, chamber):
            current_shape.move(jet_direction)
        if shape_can_fall(current_shape, chamber):
            current_shape.move("down")
        else:
            rock_settled = True
            chamber.raster_shape(current_shape)
            chamber.update_current_highest(current_shape)
            rocks_settled += 1
        if rock_settled:
            block_index = ((block_index + 1) % (len(blocks)))
            current_shape = Shape(blocks[block_index])
            chamber.add_shape_to_chamber(current_shape)
            rock_settled = False
            print(rocks_settled)
            # print(chamber)

        jet_index = ((jet_index + 1) % (len(jet_pattern)))
        jet_direction = jet_pattern[jet_index]
        
    print(chamber.current_highest)
        # current_shape.move("down")
            
        
        


def part_2():
    blocks = parse_blocks_file("day_17/blocks.txt")
    jet_pattern = open("day_17/input.txt").read().strip()
    chamber = Chamber()
    current_shape = Shape(blocks[0])
    block_index = 0
    rock_settled = False
    chamber.add_shape_to_chamber(current_shape)
    jet_index = 0
    jet_direction = jet_pattern[0]
    rocks_settled = 0
    actual_current_highest = 0
    rocks_to_settle = 1000000000000
    repeating_cycle_applied = False
    fingerprints = {}
    while rocks_settled < rocks_to_settle:
        if shape_can_move_in_direction(jet_direction, current_shape, chamber):
            current_shape.move(jet_direction)
        if shape_can_fall(current_shape, chamber):
            current_shape.move("down")
        else:
            rock_settled = True
            chamber.raster_shape(current_shape)
            chamber.update_current_highest(current_shape)
            actual_current_highest += chamber.current_highest_increment
            rocks_settled += 1
            if not repeating_cycle_applied:
                fingerprint = chamber.get_fingerprint(block_index, jet_index)
                fingerprint_record = fingerprints.get(fingerprint, None)
                if fingerprint_record is None:
                    fingerprints[fingerprint] = {
                        "rocks_settled": rocks_settled,
                        "height": chamber.current_highest,
                        "jet_index": jet_index,
                        "block_index": block_index
                    }
                else:
                    rocks_settled_in_cycle = rocks_settled - fingerprint_record["rocks_settled"]
                    height_gained_in_cycle = chamber.current_highest - fingerprint_record["height"]
                    rocks_left_to_settle = rocks_to_settle - rocks_settled
                    repeats = rocks_left_to_settle // rocks_settled_in_cycle
                    actual_current_highest = actual_current_highest + (height_gained_in_cycle * repeats)
                    rocks_settled = rocks_settled + (rocks_settled_in_cycle * repeats)
                    repeating_cycle_applied = True

        if rock_settled:
            block_index = ((block_index + 1) % (len(blocks)))
            current_shape = Shape(blocks[block_index])
            chamber.add_shape_to_chamber(current_shape)
            rock_settled = False
            print(rocks_settled)

        jet_index = ((jet_index + 1) % (len(jet_pattern)))
        jet_direction = jet_pattern[jet_index]

    print(chamber.current_highest)
    print(actual_current_highest)


def main():
    part_1()
    part_2()


if __name__ == "__main__":
    main()
