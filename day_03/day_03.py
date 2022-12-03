def char_to_priority(c: str):
    return ord(c)-96 if c.islower() else ord(c)-64+26


def part_1():
    with open("day_03/input.txt") as f:
        priorities_of_duplicates = []
        for line in f:
            line = line.strip()
            middle = int(len(line)/2)
            priorities_of_duplicates.append(
                char_to_priority(
                    set.intersection(set(line[:middle]),
                                     set(line[middle:])).pop()
                )
            )
    print("Part 1 - The sum of priorities are "
          f"{sum(priorities_of_duplicates)}")


def part_2():
    with open("day_03/input.txt") as f:
        lines = f.readlines()
        priorities_of_commons = []
        for i in range(0, len(lines), 3):
            priorities_of_commons.append(
                char_to_priority(
                    set.intersection(
                        set(lines[i].strip()),
                        set(lines[i+1].strip()),
                        set(lines[i+2].strip())
                    ).pop()
                )
            )
    print(f"Part 2 - The sum of priorities are {sum(priorities_of_commons)}")


def main():
    part_1()
    part_2()
    
    # Part 1 - oneliner
    print(sum([ord(c)-96 if c.islower()else ord(c)-38 for c in[set.intersection(set(l[:len(l)//2]),set(l[len(l)//2:])).pop()for l in open("day_03/input.txt").readlines()]]))

    # Part 2 - (the shortest of) oneliner(s)
    print(sum([ord(c)-96 if c.islower()else ord(c)-38 for c in[set.intersection(set(open("day_03/input.txt").readlines()[i].strip()),set(open("day_03/input.txt").readlines()[i+1].strip()),set(open("day_03/input.txt").readlines()[i+2].strip())).pop()for i in range(0, len(open("day_03/input.txt").readlines()),3)]]))


if __name__ == "__main__":
    main()
