def solve_part_one(input_data):
    steps = 0
    maze = {}
    zzz = False
    rows = input_data.splitlines()
    for ix, row in enumerate(rows):
        if ix == 0:
            directions = row.strip()
        if ix >= 2:
            node_key = row.split("=")[0].strip()
            node = row.split("=")[1].strip().split(",")
            node_l = node[0].replace("(", "").strip()
            node_r = node[1].replace(")", "").strip()
            node_value = node_l, node_r
            maze[node_key] = node_value
    curr_node = "AAA"
    while not zzz:
        for dir in directions:
            if dir == "R":
                curr_node = maze[curr_node][1]
            else:
                curr_node = maze[curr_node][0]
            steps += 1
            if curr_node == "ZZZ":
                return steps


def get_nr(bx):
    ax = bx[1:]
    b = bx[0]
    count = 1
    count2 = 1
    found = False
    sum = 0
    for a in ax:
        while not found:
            sum = count * a
            if sum == b * count2:
                found = True
                if ax[-1] == a:
                    return sum
            elif sum > b * count2:
                count2 += 1
            else:
                count += 1
        found = False
        b = sum
        count = 1
        count2 = 1


def solve_part_two(input_data):
    steps = 0
    maze = {}
    zzz = False
    start_nodes = []
    rows = input_data.splitlines()
    for ix, row in enumerate(rows):
        if ix == 0:
            directions = row.strip()
        if ix >= 2:
            node_key = row.split("=")[0].strip()
            node = row.split("=")[1].strip().split(",")
            node_l = node[0].replace("(", "").strip()
            node_r = node[1].replace(")", "").strip()
            node_value = node_l, node_r
            maze[node_key] = node_value
    for node in maze:
        if node[-1] == "A":
            start_nodes.append(node)
    curr_nodes = start_nodes
    repeat_nr = []
    for node in curr_nodes:
        found = False
        steps = 1
        while not found:
            for dir in directions:
                if dir == "R":
                    node = maze[node][1]
                else:
                    node = maze[node][0]
                if node[-1] == "Z":
                    found = True
                    repeat_nr.append(steps)
                steps += 1
    repeat_nr = sorted(repeat_nr, reverse=True)
    nr = get_nr(repeat_nr)
    return nr


if __name__ == "__main__":
    with open("input.txt", "r") as file:
        input_data = file.read()

    part_one_solution = solve_part_one(input_data)
    print(f"Part One Solution: {part_one_solution}")

    part_two_solution = solve_part_two(input_data)
    print(f"Part Two Solution: {part_two_solution}")
