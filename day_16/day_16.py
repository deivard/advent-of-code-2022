"""Day 16: Proboscidea Volcanium
"""

from itertools import permutations
from multiprocessing import Pool


class Valve:
    def __init__(self, name: str,
                 flow_rate: int,
                 connections: list[str],
                 opened=False) -> None:
        self.name = name
        self.flow_rate = flow_rate
        self.connections = connections
        self.opened = opened

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Valve):
            return (self.name == __o.name)
        return False


def parse_input(filename: str) -> dict:
    valves = {}

    for line in open(filename).readlines():
        line = line.strip()
        valve_name = line.split(" ")[1]
        flow_rate = int(line.split(" ")[4].split("=")[-1].replace(";", ""))
        connections = (line.replace("to valves", "to valve")
                       .split("to valve ")[-1]
                       .replace(" ", "")
                       .split(","))
        valves[valve_name] = Valve(valve_name, flow_rate, connections)

    return valves


def create_graph(valves: list[Valve]):
    valve_names = list(valves.keys())
    for valve_name in valve_names:
        opened_valve = Valve(
            valve_name + "_opened",
            valves[valve_name].flow_rate,
            valves[valve_name].connections,
            True
        )
        valves[valve_name].connections.append(opened_valve.name)
        valves[valve_name].flow_rate = 0
        valves[valve_name + "_opened"] = opened_valve

    return valves


def visit_edges(current_valve, graph, total_flow_rate,
                released_pressure, minute):
    if minute == 30:
        return released_pressure
    return max(
        [visit_edges(graph[name],
                     graph,
                     total_flow_rate+current_valve.increased_flow_rate,
                     released_pressure+total_flow_rate,
                     minute + 1)
         for name in current_valve.connections]
    )


def select_next_valve(current_valve_name, valves_of_interest,
                      graph, minutes_left):
    valve_paths = []
    for valve in valves_of_interest:
        valve_paths.append({
            "valve_name": valve,
            "path": get_closest_path_to_valve(current_valve_name, valve, graph)
        })
    valve_candidates = list(filter(lambda p: len(p["path"]) < minutes_left,
                                   valve_paths))
    best_valve = valve_candidates[0]
    best_value = valve_heuristic(graph[best_valve["valve_name"]],
                                 len(best_valve["path"]),
                                 minutes_left)
    for valve_dict in valve_candidates[1:]:
        value = valve_heuristic(graph[valve_dict["valve_name"]],
                                len(valve_dict["path"]),
                                minutes_left)
        if value > best_value:
            best_value = value
            best_valve = valve_dict

    return best_valve


def valve_heuristic(valve: Valve, travel_cost: int, minutes_left: int):
    possible_pressure_release = (valve.flow_rate
                                 * (minutes_left - travel_cost))
    return possible_pressure_release


def get_closest_path_to_valve(current_valve, target_valve, graph, path=None):
    if path is None:
        path = []
    path = path + [current_valve]
    if graph[current_valve] == graph[target_valve]:
        return path

    paths = []
    for connection in graph[current_valve].connections:
        if connection not in path:
            closest_path = get_closest_path_to_valve(
                connection, target_valve, graph, path
            )
            if closest_path is not None:
                paths.append(closest_path)

    if not len(paths):
        return None
    else:
        return min(paths, key=lambda p: len(p))


def get_non_zero_flow_valves(valves: list[Valve]):
    return [valve.name for valve in valves.values()
            if valve.flow_rate > 0]


def mp_helper(current_valve_name, valve, graph):
    return {
        "valve_name": valve,
        "path": get_closest_path_to_valve(current_valve_name, valve, graph)
    }


def get_max_pressure_p1(current_valve_name, valves_of_interest, graph,
                        total_flow_rate, released_pressure, elapsed_time):
    minutes_left = 30 - elapsed_time
    valve_paths = []
    for valve in valves_of_interest:
        valve_paths.append({
            "valve_name": valve,
            "path": get_closest_path_to_valve(current_valve_name, valve, graph)
        })
    valve_candidates = list(filter(lambda p: len(p["path"]) < minutes_left,
                                   valve_paths))
    released_pressures = []
    for valve_candidate in valve_candidates:
        new_valves_of_interest = list(filter(
            lambda v: v["valve_name"] != valve_candidate["valve_name"],
            valve_candidates
        ))
        new_valves_of_interest = [v["valve_name"]
                                  for v in new_valves_of_interest]
        task_cost = len(valve_candidate["path"])
        released_pressures.append(get_max_pressure_p1(
            valve_candidate["valve_name"],
            new_valves_of_interest,
            graph,
            total_flow_rate+graph[valve_candidate["valve_name"]].flow_rate,
            released_pressure+(total_flow_rate*task_cost),
            elapsed_time + task_cost
        ))
    released_pressure += (total_flow_rate*(30-elapsed_time))
    released_pressures.append(released_pressure)
    return max(released_pressures)


def get_possible_paths_and_pressures(
        current_valve_name, valves_of_interest, graph,
        total_flow_rate, released_pressure, elapsed_time,
        current_path=None, use_multiprocessing=False):
    if not use_multiprocessing:
        return __get_possible_paths_and_pressures(
            current_valve_name, valves_of_interest, graph,
            total_flow_rate, released_pressure, elapsed_time,
            current_path
        )
    else:
        current_path = []
        nested_paths_and_pressures = []
        args = []
        valve_candidates = []
        for valve in valves_of_interest:
            valve_candidates.append({
                "valve_name": valve,
                "path": get_closest_path_to_valve(current_valve_name, valve,
                                                  graph)
            })
        for valve_candidate in valve_candidates:
            new_valves_of_interest = [v for v in valves_of_interest
                                      if v != valve_candidate["valve_name"]]
            task_cost = len(valve_candidate["path"])
            args.append((
                valve_candidate["valve_name"],
                new_valves_of_interest,
                graph,
                total_flow_rate+graph[valve_candidate["valve_name"]].flow_rate,
                released_pressure+(total_flow_rate*task_cost),
                elapsed_time + task_cost,
                current_path + [valve_candidate["valve_name"]]
            ))

        with Pool(processes=len(args)) as p:
            nested_paths_and_pressures = p.starmap(
                __get_possible_paths_and_pressures, args
            )

        flattened_paths_and_pressures = []
        for path_list in nested_paths_and_pressures:
            flattened_paths_and_pressures.extend(path_list)

        return flattened_paths_and_pressures


def path_theoretical_remaining_flow(graph, valve_candidates, time_left):
    optimal_flow_left = 0
    for name in valve_candidates:
        optimal_flow_left += graph[name].flow_rate * time_left
    return optimal_flow_left


def __get_possible_paths_and_pressures(
        current_valve_name, valves_of_interest, graph,
        total_flow_rate, released_pressure, elapsed_time,
        current_path=None):
    if current_path is None:
        current_path = []
    minutes_left = 26 - elapsed_time
    valve_paths = []
    for valve in valves_of_interest:
        valve_paths.append({
            "valve_name": valve,
            "path": get_closest_path_to_valve(current_valve_name, valve, graph)
        })
    valve_candidates = list(filter(lambda p: len(p["path"]) < minutes_left,
                                   valve_paths))
    path_and_pressure_history = []
    for valve_candidate in valve_candidates:
        # TODO: Only evaluate if path has potential to be the best.
        new_valves_of_interest = list(filter(
            lambda v: v["valve_name"] != valve_candidate["valve_name"],
            valve_candidates
        ))
        new_valves_of_interest = [v["valve_name"]
                                  for v in new_valves_of_interest]
        task_cost = len(valve_candidate["path"])
        p = get_possible_paths_and_pressures(
            valve_candidate["valve_name"],
            new_valves_of_interest,
            graph,
            total_flow_rate+graph[valve_candidate["valve_name"]].flow_rate,
            released_pressure+(total_flow_rate*task_cost),
            elapsed_time + task_cost,
            current_path + [valve_candidate["valve_name"]]
        )
        path_and_pressure_history.extend(p)

    released_pressure += (total_flow_rate*minutes_left)
    return path_and_pressure_history + [(current_path, released_pressure)]


def part_1():
    valves_graph = parse_input("day_16/input.txt")
    valves_of_interest = get_non_zero_flow_valves(valves_graph)
    max_pressure = get_max_pressure_p1("AA", valves_of_interest,
                                       valves_graph, 0, 0, 0)
    print(f"Part 1 - The maximum possible pressure is {max_pressure}")


def find_mutualy_exclusive_paths(path_history):
    mutually_exclusives = []
    for i, (path_a, pressure_a) in enumerate(path_history):
        set_a = set(path_a)
        for path_b, pressure_b in path_history[i+1:]:
            set_b = set(path_b)
            if len(set_a.intersection(set_b)) == 0:
                mutually_exclusives.append([
                    (path_a, pressure_a),
                    (path_b, pressure_b)
                ])
    return mutually_exclusives


def part_2():
    valves_graph = parse_input("day_16/test.txt")
    valves_of_interest = get_non_zero_flow_valves(valves_graph)
    history = get_possible_paths_and_pressures(
        "AA", valves_of_interest, valves_graph,
        0, 0, 0,
        use_multiprocessing=True
    )
    print("Finding mutualy exlusive paths...")
    valid_path_pairs = find_mutualy_exclusive_paths(history)
    print(f"Found {len(valid_path_pairs)} mutually exclusive path pairs...")
    max_pair = (max(valid_path_pairs, key=lambda p: p[0][1] + p[1][1]))
    print("Part 2 - The most pressure released with the help of a trained "
          f"elephant is {max_pair[0][1]+max_pair[1][1]}.")


def main():
    part_1()
    part_2()


if __name__ == "__main__":
    main()
