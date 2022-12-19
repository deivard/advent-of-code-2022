"""Day 16: Proboscidea Volcanium
"""
import random
import matplotlib.pyplot as plt
# random.seed("Day 16")


class Valve:
    def __init__(self, name: str,
                 flow_rate: int,
                 connections: list[str],
                 opened=False) -> None:
        self.name = name
        self.increased_flow_rate = flow_rate
        self.connections = connections
        self.opened = opened
        self.pheromone = 10

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Valve):
            return (self.name == __o.name
                    and self.opened == __o.opened)
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


class Ant:
    def __init__(self, current_valve, valve_map):
        self.valve_map = valve_map
        self.current_valve = current_valve
        self.start = current_valve
        self.visited = [self.current_valve]
        self.minutes_passed = 0
        self.pressure_released = 0
        self.total_flow_rate = 0

    def move(self, alpha, beta):
        next_valve_name = self.chose_next_valve(alpha, beta)
        self.pressure_released += self.total_flow_rate
        self.current_valve = next_valve_name
        self.visited.append(self.current_valve)
        self.total_flow_rate += self.valve_map[next_valve_name].increased_flow_rate
        self.minutes_passed += 1

    def chose_next_valve(self, alpha, beta):
        probabilities = []
        for valve_name in self.valve_map[self.current_valve].connections:
            if (self.valve_map[valve_name].opened
                    and valve_name in self.visited):
                continue
            increased_flow_rate = self.valve_map[valve_name].increased_flow_rate
            pheromone = self.valve_map[valve_name].pheromone
            probabilities.append({
                "valve_name": valve_name,
                "probability": (pheromone**alpha)*((increased_flow_rate+1)**beta)
            })
        weights = [p["probability"] for p in probabilities]
        choice = random.choices(probabilities, weights=weights)[0]

        return choice["valve_name"]


def initialize_ants(num_ants, valve_map):
    return [Ant("AA", valve_map) for _ in range(num_ants)]


def create_graph(valves: list[Valve]):
    valve_names = list(valves.keys())
    for valve_name in valve_names:
        opened_valve = Valve(
            valve_name + "_opened",
            valves[valve_name].increased_flow_rate,
            valves[valve_name].connections,
            True
        )
        valves[valve_name].connections.append(opened_valve.name)
        valves[valve_name].increased_flow_rate = 0
        valves[valve_name + "_opened"] = opened_valve

    return valves


def update_pheromone(ants, graph: dict[Valve], evaporation_rate):
    for valve in graph.values():
        valve.pheromone = (1 - evaporation_rate) * valve.pheromone

    for ant in ants:
        for visited in ant.visited[1::]:
            graph[visited].pheromone += (ant.pressure_released*0.01)


def part_1():
    valves = parse_input("day_16/input.txt")

    max_time = 30
    best_in_iterations = []
    ALPHA = 0
    EVAPORATION_RATE = 0.5
    BETA = 2
    graph = create_graph(valves)
    while len(best_in_iterations) < 250:
        ants = initialize_ants(2000, graph)
        for _ in range(max_time):
            for ant in ants:
                ant.move(ALPHA, BETA)

        ants.sort(key=lambda a: a.pressure_released)
        best_ant = ants[-1]
        best_in_iterations.append(ants[-1].pressure_released)
        print(f"Best ant pressure released: {best_ant.pressure_released}")
        update_pheromone(ants, graph, EVAPORATION_RATE)

    print(max(best_in_iterations))

    plt.plot([i for i in range(len(best_in_iterations))],
             best_in_iterations)
    plt.xlabel('Iteration')
    plt.ylabel('Highest pressure released')
    plt.title("Day 16")


def part_2():
    pass


def main():
    part_1()
    part_2()


if __name__ == "__main__":
    main()
