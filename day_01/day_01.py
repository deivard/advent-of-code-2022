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
    index, inventory = max(enumerate(inventories), key=lambda enumeration: sum(enumeration[1]))
    return index, sum(inventory)


def main():
    inventories = get_inventories_from_file("day_01/input.txt")
    index, highest_calory_inventory = get_highest_calory_inventory(inventories)
    print(f"Highest calory invetory belongs to elf number {index}, with {highest_calory_inventory} calories in it.")


if __name__=="__main__":
    main()
    # One liner/code golf
    print(max([sum(map(int,i.strip().split("\n")))for i in open("day_01/input.txt").read().split("\n\n")]))
    

    
        