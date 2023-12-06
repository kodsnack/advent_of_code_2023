import re


def solve_part_one(input_data):
    sum = 1
    rows = input_data.splitlines()
    times = rows[0].split(":")[1].strip()
    times = re.sub(" +", " ", times)
    times = times.split(" ")
    dists = rows[1].split(":")[1].strip()
    dists = re.sub(" +", " ", dists)
    dists = dists.split(" ")
    for ix, time in enumerate(times):
        time = int(time)
        dist = int(dists[ix])
        count = 0
        for lap in range(0, time + 1):
            lap_time = time - lap
            lap_dist = lap_time * lap
            if lap_dist > dist:
                count += 1
        sum *= count
    return sum


def solve_part_two(input_data):
    sum = 1
    count = 0
    rows = input_data.splitlines()
    times = rows[0].split(":")[1].strip()
    times = re.sub(" +", " ", times)
    times = times.replace(" ", "")
    time = int(times)
    dists = rows[1].split(":")[1].strip()
    dists = re.sub(" +", " ", dists)
    dists = dists.replace(" ", "")
    dist = int(dists)
    for lap in range(0, time + 1):
        lap_time = time - lap
        lap_dist = lap_time * lap
        if lap_dist > dist:
            count += 1
    sum *= count
    return sum


if __name__ == "__main__":
    with open("input.txt", "r") as file:
        input_data = file.read()

    part_one_solution = solve_part_one(input_data)
    print(f"Part One Solution: {part_one_solution}")

    part_two_solution = solve_part_two(input_data)
    print(f"Part Two Solution: {part_two_solution}")
