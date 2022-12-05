"""Day 05: Supply Stacks
"""


def get_starting_state_from_file(filename: str):
    lines = []
    with open(filename) as f:
        for line in f:
            stripped_line = line.rstrip("\n")
            if len(stripped_line) == 0:
                break
            lines.append(stripped_line)

    return get_stacks_data_from_line_rows(lines)


def get_stacks_data_from_line_rows(
        line_rows: list[str],
        column_len=3,
        column_spacing=1):
    num_stacks = int(line_rows[-1].strip().split(" "*column_spacing)[-1])
    stacks = [[] for _ in range(num_stacks)]

    for line in line_rows[:-1][::-1]:
        for i in range(num_stacks):
            stack_content = line[i*(column_len+column_spacing)+1]
            if stack_content != " ":
                stacks[i].append(stack_content)

    return stacks


def find_instructions_starting_line(lines: list[str]):
    for i in range(len(lines)):
        if lines[i].startswith("move"):
            return i
    raise ValueError("No instructions found in the file.")


def parse_instruction_line(instruction_line: str):
    instruction = {}
    split_line = instruction_line.split(" ")
    for i in range(0, len(split_line), 2):
        instruction[split_line[i]] = int(split_line[i+1])

    return instruction


def get_instructions_from_file(filename: str):
    lines = open(filename).readlines()
    instruction_starting_line = find_instructions_starting_line(lines)
    instructions_unparsed = lines[instruction_starting_line:]
    instructions_parsed = [
        parse_instruction_line(instruction_line)
        for instruction_line in instructions_unparsed
    ]

    return instructions_parsed


def perform_cratemover_9000_instruction(
        instruction: dict,
        stacks: list[list[str]]):
    for _ in range(instruction["move"]):
        stacks[instruction["to"]-1].append(
            stacks[instruction["from"]-1].pop()
        )


def perform_cratemover_9001_instruction(
        instruction: dict,
        stacks: list[list[str]]):
    stacks[instruction["to"]-1].extend(
        stacks[instruction["from"]-1][-instruction["move"]:]
    )
    stacks[instruction["from"]-1] = (
        stacks[instruction["from"]-1][:-instruction["move"]]
    )


def perform_instructions_on_stacks(
        instructions: list[dict],
        stacks: list[list[str]],
        cratemover_version: int = 9000):
    if cratemover_version == 9000:
        performer_function = perform_cratemover_9000_instruction
    else:
        performer_function = perform_cratemover_9001_instruction

    for instruction in instructions:
        performer_function(instruction, stacks)

    return stacks


def stack_tops_to_string(columns: list[str]):
    return "".join([c[-1] if len(c) else " " for c in columns])


def part_1():
    starting_state = get_starting_state_from_file("day_05/input.txt")
    instructions = get_instructions_from_file("day_05/input.txt")
    end_state = perform_instructions_on_stacks(instructions, starting_state,
                                               9000)
    print("Part 1 - Supplies on top of stacks: "
          f"{stack_tops_to_string(end_state)}")


def part_2():
    starting_state = get_starting_state_from_file("day_05/input.txt")
    instructions = get_instructions_from_file("day_05/input.txt")
    end_state = perform_instructions_on_stacks(instructions, starting_state,
                                               9001)
    print("Part 2 - Supplies on top of stacks: "
          f"{stack_tops_to_string(end_state)}")


def main():
    part_1()
    part_2()


if __name__ == "__main__":
    main()
