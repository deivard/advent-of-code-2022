"""Day 19: Not Enough Minerals
"""

from dataclasses import dataclass, asdict
from math import ceil
from multiprocessing import Pool
import re
from copy import deepcopy
import time


def parse_input(filename: str):
    lines = [line.strip() for line in open(filename)]
    blueprints = [Blueprint(line) for line in lines]

    return blueprints


class Currency:
    def __init__(self, ore: int = 0, clay: int = 0,
                 obsidian: int = 0, geode: int = 0) -> None:
        self.__values = {
            "ore": ore,
            "clay": clay,
            "obsidian": obsidian,
            "geode": geode
        }

    @property
    def ore(self):
        return self.__values["ore"]

    @property
    def clay(self):
        return self.__values["clay"]

    @property
    def obsidian(self):
        return self.__values["obsidian"]

    @property
    def geode(self):
        return self.__values["geode"]

    def get(self, key: str):
        return self.__values[key]

    def __getitem__(self, key):
        return self.__values[key]

    def __setitem__(self, key, value):
        self.__values[key] = value

    def __sub__(self, other):
        return Currency(self.ore - other.ore,
                        self.clay - other.clay,
                        self.obsidian - other.obsidian,
                        self.geode - other.geode)

    def __add__(self, other):
        return Currency(self.ore + other.ore,
                        self.clay + other.clay,
                        self.obsidian + other.obsidian,
                        self.geode + other.geode)

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Currency):
            return False
        return (__o.ore == self.ore
                and __o.clay == self.clay
                and __o.obsidian == self.obsidian
                and __o.geode == self.geode)

    def __le__(self, __o: object) -> bool:
        if not isinstance(__o, Currency):
            return False
        return (self.ore <= __o.ore
                and self.clay <= __o.clay
                and self.obsidian <= __o.obsidian
                and self.geode <= __o.geode)


class Blueprint:
    def __init__(self, line: str) -> None:
        self.id = line.split(" ")[1].replace(":", "")
        self.robot_costs = {
            "clay": None,
            "ore": None,
            "obsidian": None,
            "geode": None
        }
        self.init_costs_from_line(line)
        self.max_minute_costs = self.get_max_minute_costs()
        
    def get_max_minute_costs(self):
        max_minute_costs = {
            "clay": 0,
            "ore": 0,
            "obsidian": 0,
            "geode": 0
        }
        for robot_cost in self.robot_costs:
            for currency in max_minute_costs.keys():
                max_minute_costs[currency] = max(
                    max_minute_costs[currency],
                    self.robot_costs[robot_cost][currency]
                )
        return max_minute_costs

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Blueprint):
            return False
        return (
            __o.robot_costs["ore"] == self.robot_costs["ore"]
            and __o.robot_costs["clay"] == self.robot_costs["clay"]
            and __o.robot_costs["obisidian"] == self.robot_costs["obisidian"]
            and __o.robot_costs["geode"] == self.robot_costs["geode"]
            and __o.id == self.id
        )

    def get_cost_from_string(self, string: str):
        ore_cost_re = r"[0-9]+(?= ?ore)"
        clay_cost_re = r"[0-9]+(?= ?clay)"
        obsidian_cost_re = r"[0-9]+(?= ?obsidian)"
        ore_result = re.search(ore_cost_re, string)
        clay_result = re.search(clay_cost_re, string)
        obsidian_result = re.search(obsidian_cost_re, string)

        return Currency(int(ore_result.group()) if ore_result else 0,
                        int(clay_result.group()) if clay_result else 0,
                        int(obsidian_result.group()) if obsidian_result else 0)

    def init_costs_from_line(self, line: str):
        split_line = line.split(":")[1].strip().split(".")
        self.robot_costs["ore"] = self.get_cost_from_string(split_line[0])
        self.robot_costs["clay"] = self.get_cost_from_string(split_line[1])
        self.robot_costs["obsidian"] = self.get_cost_from_string(split_line[2])
        self.robot_costs["geode"] = self.get_cost_from_string(split_line[3])


class RobotFactory:
    def __init__(self, blueprint: Blueprint, max_time=24) -> None:
        self.blueprint = blueprint
        self.max_minutes = max_time
        self.current_time = 0
        # self.minutes_left = max_time
        self.active_robots = {
            "ore": 1,
            "clay": 0,
            "obsidian": 0,
            "geode": 0
        }
        self.inventory = Currency()
        self.build_history = []
        
        clay_robot_ore_cost = self.blueprint.robot_costs["clay"].ore
        ore_robot_ore_cost = self.blueprint.robot_costs["ore"].ore
        obsidian_robot_ore_cost = self.blueprint.robot_costs["obsidian"].ore
        self.max_ore_cost = max([clay_robot_ore_cost,
                                 ore_robot_ore_cost,
                                 obsidian_robot_ore_cost])
        self.waiting_for_robot = None

    def __hash__(self) -> int:
        return hash(f"{self.current_time}{self.active_robots}{self.waiting_for_robot}"
                    f"{self.blueprint.id}")

    def min_geodes_gathered(self):
        minutes_left = self.max_minutes - self.current_time
        return self.inventory.geode + (self.active_robots["geode"]
                                       * minutes_left)

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, RobotFactory):
            return False
        return (
            __o.active_robots == self.active_robots
            and __o.inventory == self.inventory
            and __o.current_time == self.current_time
        )

    def get_buildable_robots(self):
        buildable = []
        for key, value in self.blueprint.robot_costs.items():
            if value <= self.inventory:
                buildable.append(key)
        # if not buildable:
        #     buildable.append(None)
        return buildable

    def build_robot(self, robot_key):
        # if robot_key == "geode":
        #     print(self.minutes_left)
        self.inventory = (self.inventory
                          - self.blueprint.robot_costs[robot_key])
        self.active_robots[robot_key] += 1
        self.build_history.append((robot_key, self.current_time))

    def next_state_harvest(self):
        inventory = deepcopy(self.inventory)
        for key, value in self.active_robots.items():
            inventory[key] += value
        return inventory

    def collect_harvest(self):
        for key, value in self.active_robots.items():
            self.inventory[key] += value

    def waitable_robots(self, buildable_robots=None):
        robots_to_wait_for = set()
        if buildable_robots is None:
            buildable_robots = self.get_buildable_robots()

        next_state = deepcopy(self)
        ore_per_minute = self.active_robots["ore"]
        time_to_recouperate_ore_cost = self.max_ore_cost / ore_per_minute
        for _ in range(ceil(time_to_recouperate_ore_cost)):
            next_state.collect_harvest()
            next_buildable_robots = next_state.get_buildable_robots()
            for robot in next_buildable_robots:
                if robot != "ore":
                    robots_to_wait_for.add(robot)

        robots_to_wait_for = robots_to_wait_for.difference(buildable_robots)

        return list(robots_to_wait_for)

    def get_favorable_branching_states(self):
        branched_states = []
        if self.current_time == self.max_minutes:
            return branched_states
        buildable_robots = self.get_buildable_robots()
        robots_to_wait_for = []
        # if "geode" in buildable_robots:
        #     buildable_robots = ["geode"]
        #     self.waiting_for_robot = None
        if self.waiting_for_robot is not None:
            if self.waiting_for_robot in buildable_robots:
                buildable_robots = [self.waiting_for_robot]
                self.waiting_for_robot = None
            else:
                buildable_robots = [None]
        else:
            if "geode" in buildable_robots:
                buildable_robots = ["geode"]
            else:
                robots_to_wait_for = self.waitable_robots()
                # if not robots_to_wait_for:
                #     buildable_robots = [None]
            # if (self.waitable_robots(buildable_robots)):
            #     buildable_robots.append(None)
        # elif "obsidian" in buildable_robots:
        #     try:
        #         buildable_robots.remove("clay")
            # buildable_robots = ["obsidian"]
        # if (("obsidian" not in buildable_robots
        # if not buildable_robots:
        #     buildable_robots.append(None)
        # elif (self.should_consider_waiting(buildable_robots)):
        #     buildable_robots.append(None)
        # if None not in buildable_robots:
        #     buildable_robots.append(None)
        for waitable in robots_to_wait_for:
            branched_state = deepcopy(self)
            branched_state.collect_harvest()
            branched_state.waiting_for_robot = waitable
            branched_state.current_time += 1
            branched_states.append(branched_state)
            
        for robot_key in buildable_robots:
            branched_state = deepcopy(self)
            branched_state.collect_harvest()
            if (robot_key is not None
                    and not self.is_wasteful_to_build(robot_key)):
                branched_state.build_robot(robot_key)
            branched_state.current_time += 1
            branched_states.append(branched_state)

        return branched_states

    def is_wasteful_to_build(self, robot_key):
        return (robot_key != "geode"
                and self.active_robots[robot_key]
                >= self.blueprint.max_minute_costs[robot_key])


def branch_could_be_best(current_best: RobotFactory, branch: RobotFactory):
    geodes_to_beat = current_best.min_geodes_gathered()
    num_geode_robots = branch.active_robots["geode"]
    branch_minutes_left = branch.max_minutes - branch.current_time
    best_case_increase = sum([num_geode_robots + i
                              for i in range(branch_minutes_left)])
    branch_best_potential = branch.inventory["geode"] + best_case_increase

    return branch_best_potential >= geodes_to_beat


def determine_blueprint_quality_level(blueprint: Blueprint):
    initial_factory_state = RobotFactory(blueprint)
    best_state = initial_factory_state
    open_states: list[RobotFactory] = (
        initial_factory_state.get_favorable_branching_states()
    )
    closed_states = {}
    while len(open_states):
        current_state = open_states.pop()
        closed_states[current_state] = current_state
        branches = current_state.get_favorable_branching_states()
        branches = list(filter(lambda b: branch_could_be_best(best_state, b),
                               branches))
        if (best_state.inventory.geode < current_state.inventory.geode):
                # and not branches):
            best_state = current_state
        else:
            for branch in branches:
                existing_branch = closed_states.get(branch, None)
                if existing_branch is None and branch not in open_states:
                    open_states.append(branch)

    quality_level = best_state.inventory.geode * int(blueprint.id)
    print(f"Finished blueprint {blueprint.id}")
    return quality_level


def part_1():
    blueprints = parse_input("day_19/test.txt")
    quality_levels = []
    num_processes = 1
    if num_processes == 1:
        part_1_start = time.time()
        for i, blueprint in enumerate(blueprints):
            tic = time.time()
            quality = determine_blueprint_quality_level(blueprint)
            quality_levels.append(quality)
            toc = time.time()
            time_per_blueprint = (toc - part_1_start) / (i+1)
            time_left = time_per_blueprint * (len(blueprints) - (i+1))
            print(f"Finished blueprint {i+1} in {toc-tic} seconds. "
                  f"Estimated time left: {time_left} seconds.")
    elif num_processes > 1:
        with Pool(num_processes) as p:
            quality_levels = p.map(determine_blueprint_quality_level,
                                   blueprints)
    
    print(quality_levels)
    quality_level_sum = sum(quality_levels)
    print("Part 1 - The sum of quality levels for all blueprints is "
          f"{quality_level_sum}")


def part_2():
    pass


def main():
    part_1()
    part_2()


if __name__ == "__main__":
    main()
