"""Day 19: Not Enough Minerals
"""

from dataclasses import dataclass
import re


@dataclass()
class Cost:
    ore: int = 0
    clay: int = 0
    obsidian: int = 0


class Blueprint:
    def __init__(self, line: str) -> None:
        self.id = line.split(" ")[1].replace(":", "")
        self.ore_robot_cost = None
        self.clay_robot_cost = None
        self.obisidian_robot_cost = None
        self.geode_robot_cost = None
        self.init_costs_from_line(line)

    def get_cost_from_string(self, string: str):
        ore_cost_re = r"[1-9](?= ?ore)"
        clay_cost_re = r"[1-9](?= ?clay)"
        obsidian_cost_re = r"[1-9](?= ?obsidian)"
        ore_result = re.search(ore_cost_re, string)
        clay_result = re.search(clay_cost_re, string)
        obsidian_result = re.search(obsidian_cost_re, string)

        return Cost(int(ore_result.group()) if ore_result else 0,
                    int(clay_result.group()) if clay_result else 0,
                    int(obsidian_result.group()) if obsidian_result else 0)

    def init_costs_from_line(self, line: str):
        split_line = line.split(":")[1].strip().split(".")
        self.ore_robot_cost = self.get_cost_from_string(split_line[0])
        self.clay_robot_cost = self.get_cost_from_string(split_line[1])
        self.obisidian_robot_cost = self.get_cost_from_string(split_line[2])
        self.geode_robot_cost = self.get_cost_from_string(split_line[3])


class RobotFactory:
    def __init__(self, blueprint) -> None:
        self.blueprint = blueprint
        self.active_robots = {
            "ore": 0,
            "clay": 0,
            "obsidian": 0,
            "geode": 0
        }


def parse_input(filename: str):
    lines = [line.strip() for line in open(filename)]
    blueprints = [Blueprint(line) for line in lines]

    return blueprints


def part_1():
    blueprints = parse_input("day_19/test.txt")
    pass


def part_2():
    pass


def main():
    part_1()
    part_2()


if __name__ == "__main__":
    main()
