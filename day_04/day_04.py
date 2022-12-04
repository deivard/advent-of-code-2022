from typing import Tuple


def is_subinterval(subinterval: Tuple[int, int],
                   superinterval: Tuple[int, int]):
    return subinterval[0] >= superinterval[0] \
           and subinterval[1] <= superinterval[1]


def intervals_overlap(a: Tuple[int, int], b: Tuple[int, int]):
    return (b[0] <= a[0] <= b[1] or b[0] <= a[1] <= b[1]) \
           or (a[0] <= b[0] <= a[1] or a[0] <= b[1] <= a[1])


def line_to_intervals(line: str):
    unparsed_intervals = line.strip().split(",")
    return [list(map(int, unparsed_interval.split("-")))
            for unparsed_interval in unparsed_intervals]


def part_1():
    assignments_with_subintervals = 0
    for line in open("day_04/input.txt"):
        interval_a, interval_b = line_to_intervals(line)
        if is_subinterval(interval_a, interval_b) \
           or is_subinterval(interval_b, interval_a):
            assignments_with_subintervals += 1

    print("Part 1 - Assignments with subintervals: "
          f"{assignments_with_subintervals}")


def part_2():
    assignments_with_overlap = 0
    for line in open("day_04/input.txt"):
        interval_a, interval_b = line_to_intervals(line)
        if intervals_overlap(interval_a, interval_b):
            assignments_with_overlap += 1

    print("Part 2 - Assignments with overlaps: "
          f"{assignments_with_overlap}")


def main():
    part_1()
    part_2()


if __name__ == "__main__":
    main()
