"""Day 21: Monkey Math
"""

from operator import mul, truediv, sub, add
from sympy import symbols, solve


def parse_input(filename: str):
    monkey_math = {}
    for line in open(filename).readlines():
        name, output = line.strip().split(": ")
        monkey_math[name] = output.split(" ")

    return monkey_math


def str_to_operation(string: str):
    operations = {
        "*": mul,
        "-": sub,
        "/": truediv,
        "+": add
    }
    return operations[string]


def part_1():
    monkey_math = parse_input("day_21/input.txt")
    undetermined = list(monkey_math.items())
    determined = {}
    while len(undetermined):
        monkey, output = undetermined.pop(0)
        if len(output) == 1:
            determined[monkey] = int(output[0])
        else:
            m1, operator, m2 = output
            m1_determined = determined.get(m1, None)
            m2_determined = determined.get(m2, None)
            if None in [m1_determined, m2_determined]:
                undetermined.append((monkey, output))
            else:
                operation = str_to_operation(operator)
                result = operation(m1_determined, m2_determined)
                determined[monkey] = result

    root_ouput = determined["root"]
    print(f"Part 1 - The root monkey will yell {root_ouput}.")


def part_2():
    monkey_math = parse_input("day_21/input.txt")
    expression = f"{monkey_math['root'][0]} = {monkey_math['root'][2]}"
    to_replace = [monkey_math['root'][0], monkey_math['root'][2]]
    while len(to_replace):
        current_replace = to_replace.pop(0)
        if current_replace == "humn":
            continue
        output = monkey_math[current_replace]
        if len(output) == 1:
            expression = expression.replace(current_replace, output[0])
        else:
            expression = expression.replace(current_replace,
                                            f"({' '.join(output)})")
            to_replace.extend([output[0], output[2]])

    left_hand, right_hand = expression.split("=")
    side_of_unknown = [left_hand, right_hand]["humn" in right_hand]
    other_side = [left_hand, right_hand]["humn" not in right_hand]
    expression = side_of_unknown + " - " + other_side

    # This might be considered cheating but time
    # is money friend.
    humn = symbols("humn")  # NOQA
    expr = eval(expression)
    solution = solve(expr)
    rounded_solution = round(solution[0])

    print(f"Part 2 - The number to yell is {rounded_solution}.")


def main():
    part_1()
    part_2()


if __name__ == "__main__":
    main()
