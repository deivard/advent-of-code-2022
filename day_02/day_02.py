"""2022/12/02 - Rock, Paper, Scissors
"""

from enum import IntEnum


class Choice(IntEnum):
    """Integer representation of the different choices available in the game
    Rock, Paper, Scissors.
    NOTE: The value for each choice is important since this is used to
    determine which choice that won.
    """
    ROCK = 0
    PAPER = 1
    SCISSOR = 2


class MatchOutcome(IntEnum):
    """Integer representation of the different match outcomes available in the
    game Rock, Paper, Scissors.
    """
    LOSE = 0
    DRAW = 1
    WIN = 2


POINT_MAPPINGS = {
    "choice": {
        Choice.ROCK: 1,
        Choice.PAPER: 2,
        Choice.SCISSOR: 3,
    },
    "outcome": {
        MatchOutcome.LOSE: 0,
        MatchOutcome.DRAW: 3,
        MatchOutcome.WIN: 6,
    }
}


STRATEGY_TRANSLATIONS_P1 = {
    "A": Choice.ROCK,
    "B": Choice.PAPER,
    "C": Choice.SCISSOR,
    "X": Choice.ROCK,
    "Y": Choice.PAPER,
    "Z": Choice.SCISSOR,
}


STRATEGY_TRANSLATIONS_P2 = {
    "A": Choice.ROCK,
    "B": Choice.PAPER,
    "C": Choice.SCISSOR,
    "X": MatchOutcome.LOSE,
    "Y": MatchOutcome.DRAW,
    "Z": MatchOutcome.WIN
}


def translate_instruction_p1(instruction: str):
    return STRATEGY_TRANSLATIONS_P1[str(instruction)]


def translate_instruction_p2(instruction: str):
    return STRATEGY_TRANSLATIONS_P2[str(instruction)]


def calculate_score(choice: Choice, outcome: MatchOutcome):
    return (POINT_MAPPINGS["choice"][choice]
            + POINT_MAPPINGS["outcome"][outcome])


def determine_outcome(player_choice: Choice, opponent_choice: Choice):
    if opponent_choice == player_choice:
        return MatchOutcome.DRAW
    elif opponent_choice == ((player_choice - 1) % 3):
        return MatchOutcome.WIN
    else:
        return MatchOutcome.LOSE


def determine_choice_needed_for_outcome(
            opponent_choice: Choice, desired_outcome: MatchOutcome
        ):
    if desired_outcome == MatchOutcome.LOSE:
        return (opponent_choice - 1) % 3
    elif desired_outcome == MatchOutcome.DRAW:
        return opponent_choice
    else:
        return (opponent_choice + 1) % 3


def evaluate_strategy_guide_p1(filename: str):
    total_score = 0
    with open(filename) as f:
        for line in f:
            opponent_choice, player_choice = map(
                translate_instruction_p1, line.strip().split()
            )
            player_outcome = determine_outcome(player_choice, opponent_choice)
            match_points = calculate_score(player_choice, player_outcome)
            total_score += match_points

    return total_score


def evaluate_strategy_guide_p2(filename: str):
    total_score = 0
    with open(filename) as f:
        for line in f:
            opponent_choice, desired_outcome = map(
                translate_instruction_p2, line.strip().split()
            )
            player_choice = determine_choice_needed_for_outcome(
                opponent_choice, desired_outcome
            )
            match_points = calculate_score(player_choice, desired_outcome)
            total_score += match_points

    return total_score


def part_1():
    total_score = evaluate_strategy_guide_p1("day_02/input.txt")
    print("Part 1 - Total score when following the strategy guide is "
          f"{total_score}")


def part_2():
    total_score = evaluate_strategy_guide_p2("day_02/input.txt")
    print("Part 2 - Total score when following the strategy guide is "
          f"{total_score}")


def main():
    part_1()
    part_2()


if __name__ == "__main__":
    main()
