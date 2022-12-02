def get_inventories_from_file(filename):
    with open(filename) as f:
        inventories = []
        inventory = []
        for line in f:
            if line == "\n":
                inventories.append(inventory)
                inventory = []
            else:
                inventory.append(int(line.strip()))

    return inventories


def get_highest_calory_inventory(inventories):
    index, inventory = max(
        enumerate(inventories),
        key=lambda enumeration: sum(enumeration[1])
    )
    return index, sum(inventory)


def get_n_highest_calory_inventories(inventories, n):
    inventories_sorted = sorted(map(sum, inventories))
    return inventories_sorted[-n:]


def part_1():
    inventories = get_inventories_from_file("day_01/input.txt")
    index, highest_calory_inventory = get_highest_calory_inventory(inventories)
    print(f"Highest calory invetory belongs to elf number {index}, with "
          f"{highest_calory_inventory} calories in it.")


def part_2():
    inventories = get_inventories_from_file("day_01/input.txt")
    highest_calory_inventories = get_n_highest_calory_inventories(
        inventories, 3
    )
    print(sum(highest_calory_inventories))


if __name__ == "__main__":
    part_1()
    # Part 1 - One liner/code golf
    print(max([sum(map(int,i.strip().split("\n")))for i in open("day_01/input.txt").read().split("\n\n")]))

    part_2()
    # Part 2 - One liner/code golf
    print(sum(sorted([sum(map(int,i.strip().split("\n")))for i in open("day_01/input.txt").read().split("\n\n")])[-3:]))
