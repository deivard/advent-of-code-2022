"""Day 22: Monkey Map
"""

from copy import copy, deepcopy
import re
from typing import List


def parse_input(filename: str):
    board_unparsed, instructions = open(filename).read().split("\n\n")
    board = []
    for row in board_unparsed.split("\n"):
        board.append(list(row.replace("\n", "")))

    max_width = len(max(board, key=len))
    for row in board:
        remaining = max_width - len(row)
        row.extend([" "]*remaining)

    instruction_re = r"\d+|\w"
    instructions = re.findall(instruction_re, instructions.strip())

    return board, instructions


class Player:
    MOVEMENT_MAP = {
        "E": (0, 1),
        "S": (1, 0),
        "W": (0, -1),
        "N": (-1, 0),
    }
    ORIENTATION_MAP = {
        "L": -1,
        "R": 1
    }
    ORIENTATIONS = ["E", "S", "W", "N"]

    def __init__(self, row, column) -> None:
        self.row = row
        self.column = column
        self.orientation = "E"

    def change_orientation(self, direction: str):
        current_index = Player.ORIENTATIONS.index(self.orientation)
        new_orientation_index = (
            (current_index + Player.ORIENTATION_MAP[direction])
            % len(Player.ORIENTATIONS)
        )
        self.orientation = Player.ORIENTATIONS[new_orientation_index]

    def __next_step(self, movement, board, position=None):
        if position is None:
            position = (self.row, self.column)
        return ((position[0] + movement[0]) % len(board),
                (position[1] + movement[1]) % len(board[position[0]]))

    def move(self, steps: int, board: List[List[str]]):
        movement = Player.MOVEMENT_MAP[self.orientation]
        steps_left = steps
        while steps_left:
            next_step = self.__next_step(movement, board)
            while board[next_step[0]][next_step[1]] == " ":
                next_step = self.__next_step(movement, board, next_step)
            if board[next_step[0]][next_step[1]] == ".":
                self.row, self.column = next_step
                steps_left -= 1
            elif board[next_step[0]][next_step[1]] == "#":
                steps_left = 0


class HardcodedCube:
    """
        111|222
        111|222
        111|222
        ---
        333
        333
        333
        ---
    444|555
    444|555
    444|555
    ---
    666
    666
    666
    1 = top
    2 = right
    3 = front
    4 = left
    5 = bottom
    6 = back
    Translations:
        (1) Top:
            To (2) right: if column > max (ori E) -> ori E, row = row, column = column
            To (4) left: if column < 0 (ori W) -> 
            
            


            To (3) left: column < 0, orientation W: to (3) left, top row num -> left column,
                         new orientation = S.
            To (4) front: row > max, orientation S: to (4) front, same column, row 0,
                          same orientation
            To (6) right: column > max, orientation E: to (6) right, row -> -(row+1?), column=max,
                          new orientation = W
            To (2) back: row < 0, orientation N: to (2) back, row=0, same column,
                         new orientation = N
        (2) Back:
            To (3) left: column > max, orientation E: to (3) left, same row, column 0,
                         same orientation
            To (6) right: column < 0, orientation W: to (6) right, 
        
    
    """
    def __init__(self) -> None:
        self.top = """
            ...#
            .#..
            #...
            ....
        """
        
def print_state(player, board):
    copied_board = deepcopy(board)
    copied_board[player.row][player.column] = "@"
    rows = ["".join(row) for row in copied_board]
    print("_"*len(board[0]))
    for row in rows:
        print(row)


def get_starting_position(board):
    for i, row in enumerate(board):
        for j, value in enumerate(row):
            if value == ".":
                return (i, j)
    raise ValueError("Could not find starting position on board.")


def get_final_password(player: Player):
    facing_values = {
        "E": 0,
        "S": 1,
        "W": 2,
        "N": 3
    }
    return ((1000 * (player.row + 1))
            + (4 * (player.column + 1))
            + facing_values[player.orientation])


def part_1():
    board, instructions = parse_input("day_22/input.txt")
    starting_pos = get_starting_position(board)
    player = Player(starting_pos[0], starting_pos[1])
    for instruction in instructions:
        if instruction.isnumeric():
            player.move(int(instruction), board)
        else:
            player.change_orientation(instruction)

    final_password = get_final_password(player)
    print(final_password)


def part_2():
    pass


def main():
    part_1()
    part_2()


if __name__ == "__main__":
    main()
