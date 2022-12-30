"""Day 19: Not Enough Minerals
"""

from multiprocessing import Pool, cpu_count
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
        self.values = {
            "ore": ore,
            "clay": clay,
            "obsidian": obsidian,
            "geode": geode
        }

    @property
    def ore(self):
        return self.values["ore"]

    @property
    def clay(self):
        return self.values["clay"]

    @property
    def obsidian(self):
        return self.values["obsidian"]

    @property
    def geode(self):
        return self.values["geode"]

    def get(self, key: str):
        return self.values[key]

    def __getitem__(self, key):
        return self.values[key]

    def __setitem__(self, key, value):
        self.values[key] = value

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

    def __lt__(self, __o: object) -> bool:
        if not isinstance(__o, Currency):
            return False
        return (self.ore < __o.ore
                or self.clay < __o.clay
                or self.obsidian < __o.obsidian
                or self.geode < __o.geode)


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
        return hash(f"{self.current_time}{self.active_robots}"
                    f"{self.waiting_for_robot}{self.blueprint.id}")

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
            if not self.inventory < value:
                buildable.append(key)
        return buildable

    def build_robot(self, robot_key):
        self.inventory = (self.inventory
                          - self.blueprint.robot_costs[robot_key])
        self.active_robots[robot_key] += 1
        self.build_history.append(("B: " + str(robot_key), self.current_time))

    def collect_harvest(self):
        for key, value in self.active_robots.items():
            self.inventory[key] += value

    def is_wasteful_to_build(self, robot_key):
        return (robot_key != "geode"
                and self.active_robots[robot_key]
                >= self.blueprint.max_minute_costs[robot_key])

    def get_branching_states(self):
        branchable_states = []
        if self.current_time == self.max_minutes:
            return []
            # lool pruttkod nu löser jag dig ja  //Anna
        if self.waiting_for_robot is None:
            for robot in self.blueprint.robot_costs.keys():
                if not self.is_wasteful_to_build(robot):
                    branchable_states.append(robot)
        branched_states = []
        for key in branchable_states:
            branched_state = deepcopy(self)
            branched_state.waiting_for_robot = key
            branched_state.fast_forward_until_next_build()
            branched_states.append(branched_state)

        return branched_states

    def can_build_robot(self, robot_key):
        cost = self.blueprint.robot_costs[robot_key]
        for key, value in cost.values.items():
            if value != 0 and value > self.inventory.values[key]:
                return False
        return True

    def fast_forward_until_next_build(self):
        while not self.can_build_robot(self.waiting_for_robot):
            self.collect_harvest()
            self.current_time += 1
            self.build_history.append(("W: " + str(self.waiting_for_robot),
                                       self.current_time))
            if self.current_time == self.max_minutes:
                return

        self.collect_harvest()
        self.current_time += 1
        self.build_robot(self.waiting_for_robot)
        self.waiting_for_robot = None


def branch_could_be_best(current_best: RobotFactory, branch: RobotFactory):
    geodes_to_beat = current_best.min_geodes_gathered()
    num_geode_robots = branch.active_robots["geode"]
    branch_minutes_left = branch.max_minutes - branch.current_time
    best_case_increase = sum([num_geode_robots + i
                              for i in range(branch_minutes_left)])
    branch_best_potential = branch.inventory["geode"] + best_case_increase

    return branch_best_potential >= geodes_to_beat


def determine_blueprint_quality_level(blueprint: Blueprint,
                                      time_limit: int = 24):
    max_geodes = determine_blueprint_max_geodes(blueprint, time_limit)
    quality_level = max_geodes * int(blueprint.id)
    return quality_level


def determine_blueprint_max_geodes(blueprint: Blueprint, time_limit=32):
    initial_state = RobotFactory(blueprint, time_limit)
    best_state = initial_state
    open_states: list[RobotFactory] = initial_state.get_branching_states()
    closed_states = {}
    while len(open_states):
        current_state = open_states.pop()
        closed_states[current_state] = current_state
        branches = current_state.get_branching_states()
        branches = list(filter(lambda b: branch_could_be_best(best_state, b),
                               branches))
        if best_state.inventory.geode < current_state.inventory.geode:
            best_state = current_state
        for branch in branches:
            existing_branch = closed_states.get(branch, None)
            if existing_branch is None and branch not in open_states:
                open_states.append(branch)

    print(f"Finished blueprint {blueprint.id}")
    return best_state.inventory.geode


def part_1(num_processes=1):
    blueprints = parse_input("day_19/input.txt")
    quality_levels = []
    if num_processes == 1:
        part_1_start = time.time()
        for i, blueprint in enumerate(blueprints):
            tic = time.time()
            quality = determine_blueprint_quality_level(blueprint, 24)
            quality_levels.append(quality)
            toc = time.time()
            time_per_blueprint = (toc - part_1_start) / (i+1)
            time_left = time_per_blueprint * (len(blueprints) - (i+1))
            print(f"Finished blueprint {i+1} in {toc-tic} seconds. "
                  f"Estimated time left: {time_left} seconds.")
    elif num_processes > 1:
        with Pool(num_processes) as p:
            quality_levels = p.starmap(determine_blueprint_quality_level,
                                       zip(blueprints, [24]*len(blueprints)))

    print(quality_levels)
    quality_level_sum = sum(quality_levels)
    print("Part 1 - The sum of quality levels for all blueprints is "
          f"{quality_level_sum}")


def part_2(num_processes=1):
    blueprints = parse_input("day_19/input.txt")
    blueprints = blueprints[:3]
    max_geodes = []
    if num_processes == 1:
        part_1_start = time.time()
        for i, blueprint in enumerate(blueprints):
            tic = time.time()
            quality = determine_blueprint_max_geodes(blueprint, 32)
            max_geodes.append(quality)
            toc = time.time()
            time_per_blueprint = (toc - part_1_start) / (i+1)
            time_left = time_per_blueprint * (len(blueprints) - (i+1))
            print(f"Finished blueprint {i+1} in {toc-tic} seconds. "
                  f"Estimated time left: {time_left} seconds.")
    elif num_processes > 1:
        with Pool(num_processes) as p:
            max_geodes = p.starmap(determine_blueprint_max_geodes,
                                   zip(blueprints, [32]*len(blueprints)))

    print(max_geodes)
    max_geode_prod = max_geodes[0] * max_geodes[1] * max_geodes[2]
    print("Part 2 - The product of max geodes for 3 first blueprints is "
          f"{max_geode_prod}")


def main():
    num_processors = cpu_count()
    part_1(num_processors)
    part_2(min(num_processors, 3))


if __name__ == "__main__":
    main()
