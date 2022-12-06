"""Day 06: Tuning Trouble
"""


def find_first_unique_sequence_index(
    characters: str,
    sequence_len: int
):
    """Finds the endpoint index for the first occurence of a unique
    sequence of _sequence_len_ length in the given string.

    Args:
        characters (str): String in which the unique sequence is located.
        sequence_len (int): The length of the unique sequence that should
                            be found.

    Returns:
        int: The ending index of the unique sequence.
    """
    for i in range(len(characters)-sequence_len):
        char_set = set(characters[i:i+sequence_len])
        if len(char_set) == sequence_len:
            return i+sequence_len
    raise ValueError(f"No unique sequence of length {sequence_len} "
                     "found in the given character string.")


def part_1():
    characters = open("day_06/input.txt").read().strip()
    index = find_first_unique_sequence_index(characters, 4)
    print("The first occuring unique sequence of length 4 "
          f"ends at index {index}.")


def part_2():
    characters = open("day_06/input.txt").read().strip()
    index = find_first_unique_sequence_index(characters, 14)
    print("The first occuring unique sequence of length 14 "
          f"ends at index {index}.")


def main():
    part_1()
    part_2()


if __name__ == "__main__":
    main()
