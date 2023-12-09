def solve_part_one(input_data):
    values = []
    temp_values = []
    temp_number = []
    final = []
    rows = input_data.splitlines()
    for row in rows:
        row = row.split(" ")
        values.append(row)
    values = [[int(x) for x in inner_list] for inner_list in values]
    for list in values:
        temp_values.append(list)
        done = False
        while not done:
            for ix, value in enumerate(list):
                if ix != len(list) - 1:
                    tmp = list[ix + 1] - value
                    temp_number.append(tmp)
                    done = all(x == 0 for x in temp_number)
            temp_values.append(temp_number)
            list = temp_number
            temp_number = []
    stop = False
    tmp_val = 0
    next_val = 0
    for value in temp_values[::-1]:
        last = value[-1]
        if last == 0 and stop:
            final.append(next_val)
            next_val = 0
            tmp_val = 0
        if last == 0 and not stop:
            stop = True
        next_val = last + tmp_val
        tmp_val = next_val
    final.append(next_val)

    return sum(final)


def solve_part_two(input_data):
    values = []
    temp_values = []
    temp_number = []
    final = []
    rows = input_data.splitlines()
    for row in rows:
        row = row.split(" ")
        values.append(row)
    values = [[int(x) for x in inner_list] for inner_list in values]
    for list in values:
        temp_values.append(list)
        done = False
        while not done:
            for ix, value in enumerate(list):
                if ix != len(list) - 1:
                    tmp = list[ix + 1] - value
                    temp_number.append(tmp)
                    done = all(x == 0 for x in temp_number)
            temp_values.append(temp_number)
            list = temp_number
            temp_number = []
    stop = False
    tmp_val = 0
    next_val = 0
    for value in temp_values[::-1]:
        first = value[0]
        done1 = all(x == 0 for x in value)
        if done1 and stop:
            final.append(next_val)
            next_val = 0
            tmp_val = 0
        if done1 and not stop:
            stop = True
        next_val = first - tmp_val
        tmp_val = next_val
    final.append(next_val)
    return sum(final)


if __name__ == "__main__":
    with open("input.txt", "r") as file:
        input_data = file.read()

    part_one_solution = solve_part_one(input_data)
    print(f"Part One Solution: {part_one_solution}")

    part_two_solution = solve_part_two(input_data)
    print(f"Part Two Solution: {part_two_solution}")
