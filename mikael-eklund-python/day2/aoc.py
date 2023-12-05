def solve_part_one(input_data):
    colors = {
        "green": 0,
        "blue": 0,
        "red": 0,
    }
    match_colors = {
        "green": 13,
        "blue": 14,
        "red": 12,
    }
    sum = 0
    game = 1
    for row in input_data.splitlines():
        row = row.split(":")[1].strip()
        row = row.split(";")
        check = True
        for item in row:
            items = item.split(",")
            for i in items:
                i = i.strip()
                i = i.split(" ")
                color = i[1].strip()
                qt = i[0].strip()
                colors[color] = int(qt)
            for key, value in match_colors.items():
                if value < colors[key]:
                    check = False
                else:
                    pass
            colors = {
                "green": 0,
                "blue": 0,
                "red": 0,
            }
        if check:
            sum += game
        game += 1

    return sum


def solve_part_two(input_data):
    colors = {
        "green": 0,
        "blue": 0,
        "red": 0,
    }
    match_colors = {
        "green": 13,
        "blue": 14,
        "red": 12,
    }
    sum = 0
    game = 1
    for row in input_data.splitlines():
        row = row.split(":")[1].strip()
        row = row.split(";")
        check = True
        print(game)
        for item in row:
            items = item.split(",")
            for i in items:
                i = i.strip()
                i = i.split(" ")
                color = i[1].strip()
                qt = i[0].strip()
                if int(qt) > colors[color]:
                    colors[color] = int(qt)
            print(colors)
        csum = 1
        for key, value in colors.items():
            print(value)
            csum = csum * value
        sum += csum
        colors = {
            "green": 0,
            "blue": 0,
            "red": 0,
        }
        game += 1
    return sum


if __name__ == "__main__":
    with open("input.txt", "r") as file:
        input_data = file.read()

    part_one_solution = solve_part_one(input_data)
    print(f"Part One Solution: {part_one_solution}")

    part_two_solution = solve_part_two(input_data)
    print(f"Part Two Solution: {part_two_solution}")
