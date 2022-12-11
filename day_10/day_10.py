"""Day 10: Cathode-Ray Tube
"""


from functools import partial
from typing import Optional


class Instruction:
    EXECUTION_TIMES = {
        "addx": 2,
        "noop": 1
    }

    def __init__(self, name: str, argument: Optional[object] = None) -> None:
        self.name = name
        self.argument = argument
        self.execution_time = Instruction.EXECUTION_TIMES[self.name]
        self.completes_on_cycle = None


class CPU:
    def __init__(self, instructions: list[str]) -> None:
        self.registers = {
            "x": 1
        }
        self.__running_instruction = None
        self.cycle = 0
        self.__end_of_cycle_callbacks = []
        self.__instructions_list = self.__parse_instructions(instructions)
        self.__instructions_iterator = iter(self.__instructions_list)
        self.out_of_instructions = False

    def add_end_of_cycle_callback(self, callback_fn):
        self.__end_of_cycle_callbacks.append(callback_fn)

    def __parse_instruction_line(self, line: str):
        command = line.strip().split(" ")
        return Instruction(
            name=command[0],
            argument=int(command[1]) if len(command) > 1 else None,
        )

    def __parse_instructions(self, instructions: list[str]):
        return [self.__parse_instruction_line(line) for line in instructions]

    def __an_instruction_has_finished(self):
        return self.__running_instruction is not None \
               and self.__running_instruction.completes_on_cycle == self.cycle

    def __handle_finished_instruction(self):
        if self.__running_instruction.argument is not None:
            self.registers["x"] += self.__running_instruction.argument
        self.__running_instruction = None

    def instruction_is_running(self):
        return self.__running_instruction is not None

    def __run_next_instruction(self):
        instruction = next(self.__instructions_iterator, None)
        if instruction is None:
            self.out_of_instructions = True
        else:
            instruction.completes_on_cycle = (
                self.cycle + instruction.execution_time
            )
        self.__running_instruction = instruction

    def start(self):
        while not self.out_of_instructions:
            if self.__an_instruction_has_finished():
                self.__handle_finished_instruction()

            if not self.instruction_is_running():
                self.__run_next_instruction()

            for callback in self.__end_of_cycle_callbacks:
                callback(self)
            self.cycle += 1


def record_register_history(history_list: list, register: str, cpu: CPU):
    history_list.append(cpu.registers[register])


def sum_of_signal_strengths(register_x_history: list[int],
                            signals_of_interest: list[int]):
    return sum([register_x_history[i]*(i+1) for i in signals_of_interest])


def part_1():
    instruction_lines = open("day_10/input.txt").readlines()
    cpu = CPU(instruction_lines)
    register_x_history = []
    cpu.add_end_of_cycle_callback(
        partial(record_register_history, register_x_history, "x")
    )
    cpu.start()

    signals_of_interest = [19] + list(range(59, len(register_x_history), 40))
    p1_solution = sum_of_signal_strengths(
        register_x_history,
        signals_of_interest
    )
    print("Part 1 - The sum of signal strengths during the cycles of "
          f"interesest is {p1_solution}")


def update_crt_screen(screen: list[str], cpu: CPU):
    if abs((cpu.cycle % 40) - cpu.registers["x"]) < 2:
        screen[cpu.cycle] = "#"


def part_2():
    screen_height = 6
    screen_width = 40
    screen = ["." for _ in range(screen_width*screen_height)]

    instruction_lines = open("day_10/input.txt").readlines()
    cpu = CPU(instruction_lines)
    cpu.add_end_of_cycle_callback(
        partial(update_crt_screen, screen)
    )
    cpu.start()

    print("Part 2 - CRT Screen is displaying: ")
    for i in range(screen_height):
        print("".join(screen[i*screen_width: (i+1)*screen_width]))


def main():
    part_1()
    part_2()


if __name__ == "__main__":
    main()
