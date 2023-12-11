from itertools import combinations


def check_empty_row(row):
    for char in row:
        if char != ".":
            return False
    return True


def find_coordinates(lst):
    coordinates = []
    for i in range(len(lst)):
        for j in range(len(lst[i])):
            if lst[i][j] == "#":
                coordinates.append((i, j))
    return coordinates


def solve_part_one(input_data):
    universe = []
    new_universe = []
    cords = []
    rows = input_data.splitlines()
    row_length = len(rows[0])
    for row in rows:
        row = row.strip()
        row = list(row)
        universe.append(row)
    for ix, row in enumerate(universe):
        if check_empty_row(row):
            new_row = row_length * ["."]
            new_universe.append(row)
            new_universe.append(new_row)
        else:
            new_universe.append(row)
    universe = new_universe
    nrof_rows = len(new_universe)
    test_row = ""
    empty_rows = []
    for row in range(0, row_length):
        for col in range(0, nrof_rows):
            test_row += new_universe[col][row]
        if check_empty_row(test_row):
            empty_rows.append(row)
        test_row = ""
    for ix, row in enumerate(empty_rows):
        for row1 in universe:
            row1.insert(row + ix + 1, ".")
    cords = find_coordinates(universe)
    sum = 0
    pairs = list(combinations(cords, 2))
    for pair in pairs:
        x = abs(pair[0][0] - pair[1][0])
        y = abs(pair[0][1] - pair[1][1])
        sum += x + y
    return sum


def is_col_between(coord1, coord2, col):
    min_col = min(coord1[0], coord2[0])
    max_col = max(coord1[0], coord2[0])
    return min_col < col < max_col


def is_row_between(coord1, coord2, row):
    min_row = min(coord1[1], coord2[1])
    max_row = max(coord1[1], coord2[1])
    return min_row < row < max_row


def solve_part_two(input_data):
    universe = []
    cords = []
    mill_row = []
    mill_col = []
    rows = input_data.splitlines()
    row_length = len(rows[0])
    for row in rows:
        row = row.strip()
        row = list(row)
        universe.append(row)
    for ix, row in enumerate(universe):
        if check_empty_row(row):
            mill_row.append(ix)
    nrof_rows = len(universe)
    test_row = ""
    for row in range(0, row_length):
        for col in range(0, nrof_rows):
            test_row += universe[col][row]
        if check_empty_row(test_row):
            mill_col.append(row)
        test_row = ""
    cords = find_coordinates(universe)
    sum = 0
    pairs = list(combinations(cords, 2))
    x = 0
    y = 0
    for pair in pairs:
        x = abs(pair[0][0] - pair[1][0])
        y = abs(pair[0][1] - pair[1][1])
        for col in mill_col:
            if is_row_between(pair[0], pair[1], col):
                x += 999999
        for row in mill_row:
            if is_col_between(pair[0], pair[1], row):
                y += 999999
        sum += x + y
        x = 0
        y = 0
    return sum


if __name__ == "__main__":
    with open("input.txt", "r") as file:
        input_data = file.read()

    part_one_solution = solve_part_one(input_data)
    print(f"Part One Solution: {part_one_solution}")

    part_two_solution = solve_part_two(input_data)
    print(f"Part Two Solution: {part_two_solution}")
