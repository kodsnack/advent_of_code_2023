def createseed(seed, nr):
    found = False
    for item in seed:
        dest = item[0]
        source = item[1]
        range1 = item[2]
        diff = dest - source
        if source <= nr <= source + range1 and not found:
            found = True
            final_dest = nr + diff
            return final_dest
    if found:
        pass
    else:
        final_dest = nr
    return final_dest


def solve_part_one(input_data):
    seeds = []
    soil = []
    fertilizer = []
    water = []
    light = []
    temperature = []
    humidity = []
    location = []

    for row in input_data.splitlines():
        if len(row) > 0:
            if ":" in row:
                name = row.split(":")[0]
                if name == "seeds":
                    numbers = row.split(":")[1].strip()
                    seeds = [int(num) for num in numbers.split()]
                else:
                    curr_name = name.split("-")[-1].strip().split(" ")[0]
            else:
                if curr_name == "soil":
                    soil_t = [int(num) for num in row.split()]
                    soil.append(soil_t)
                elif curr_name == "fertilizer":
                    fertilizer_t = [int(num) for num in row.split()]
                    fertilizer.append(fertilizer_t)
                elif curr_name == "water":
                    water_t = [int(num) for num in row.split()]
                    water.append(water_t)
                elif curr_name == "light":
                    light_t = [int(num) for num in row.split()]
                    light.append(light_t)
                elif curr_name == "temperature":
                    temperature_t = [int(num) for num in row.split()]
                    temperature.append(temperature_t)
                elif curr_name == "humidity":
                    humidity_t = [int(num) for num in row.split()]
                    humidity.append(humidity_t)
                elif curr_name == "location":
                    location_t = [int(num) for num in row.split()]
                    location.append(location_t)
    tmp_seed = []
    for nr in seeds:
        soil1 = createseed(soil, nr)
        tmp_seed.append(soil1)
    seeds = tmp_seed
    tmp_seed = []
    for nr in seeds:
        fertilizer1 = createseed(fertilizer, nr)
        tmp_seed.append(fertilizer1)
    seeds = tmp_seed
    tmp_seed = []
    for nr in seeds:
        water1 = createseed(water, nr)
        tmp_seed.append(water1)
    seeds = tmp_seed
    tmp_seed = []
    for nr in seeds:
        light1 = createseed(light, nr)
        tmp_seed.append(light1)
    seeds = tmp_seed
    tmp_seed = []
    for nr in seeds:
        temperature1 = createseed(temperature, nr)
        tmp_seed.append(temperature1)
    seeds = tmp_seed
    tmp_seed = []
    for nr in seeds:
        humidity1 = createseed(humidity, nr)
        tmp_seed.append(humidity1)
    seeds = tmp_seed
    tmp_seed = []
    for nr in seeds:
        location1 = createseed(location, nr)
        tmp_seed.append(location1)
    min_val = 1000000000000
    for item in tmp_seed:
        if item < min_val:
            min_val = item

    return min_val


def solve_part_two(input_data):
    seeds = []
    soil = []
    fertilizer = []
    water = []
    light = []
    temperature = []
    humidity = []
    location = []

    for row in input_data.splitlines():
        if len(row) > 0:
            if ":" in row:
                name = row.split(":")[0]
                if name == "seeds":
                    numbers = row.split(":")[1].strip()
                    seeds = [int(num) for num in numbers.split()]
                else:
                    curr_name = name.split("-")[-1].strip().split(" ")[0]
            else:
                if curr_name == "soil":
                    soil_t = [int(num) for num in row.split()]
                    soil.append(soil_t)
                elif curr_name == "fertilizer":
                    fertilizer_t = [int(num) for num in row.split()]
                    fertilizer.append(fertilizer_t)
                elif curr_name == "water":
                    water_t = [int(num) for num in row.split()]
                    water.append(water_t)
                elif curr_name == "light":
                    light_t = [int(num) for num in row.split()]
                    light.append(light_t)
                elif curr_name == "temperature":
                    temperature_t = [int(num) for num in row.split()]
                    temperature.append(temperature_t)
                elif curr_name == "humidity":
                    humidity_t = [int(num) for num in row.split()]
                    humidity.append(humidity_t)
                elif curr_name == "location":
                    location_t = [int(num) for num in row.split()]
                    location.append(location_t)
    sum = 1000000000
    for ix, seed in enumerate(seeds[::2]):
        end = 0
        start = seed
        end = start + seeds[ix * 2 + 1]
        for nr in range(start, end):
            soil1 = createseed(soil, nr)
            fertilizer1 = createseed(fertilizer, soil1)
            water1 = createseed(water, fertilizer1)
            light1 = createseed(light, water1)
            temperature1 = createseed(temperature, light1)
            humidity1 = createseed(humidity, temperature1)
            location1 = createseed(location, humidity1)
            if location1 < sum:
                sum = location1
    return sum


if __name__ == "__main__":
    with open("input.txt", "r") as file:
        input_data = file.read()

    part_one_solution = solve_part_one(input_data)
    print(f"Part One Solution: {part_one_solution}")

    part_two_solution = solve_part_two(input_data)
    print(f"Part Two Solution: {part_two_solution}")
