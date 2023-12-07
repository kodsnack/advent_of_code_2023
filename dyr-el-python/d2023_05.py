from aoc_prepare import PrepareAoc


def parse(inp):
    result = dict()
    sections = inp.split("\n\n")
    for section in sections:
        if section.startswith("seeds: "):
            result["seeds"] = list(map(int, section[7:].split()))
        else:
            map_name = list(section.splitlines())[0][:-1]
            result[map_name] = list()
            for line in list(section.splitlines())[1:]:
                dest, source, length = map(int, line.split())
                result[map_name].append((dest, source, length))
    return result


CONVERSION_TYPES = ("seed-to-soil map", "soil-to-fertilizer map", "fertilizer-to-water map",
                    "water-to-light map", "light-to-temperature map", "temperature-to-humidity map",
                    "humidity-to-location map")


def convert(seed, mp):
    for conversion_type in CONVERSION_TYPES:
        the_map = mp[conversion_type]
        for dest, source, length in the_map:
            if source <= seed < source + length:
                seed = seed - source + dest
                break
    return seed


def convert_ranges(seed, mp):
    seeds = [seed]
    for conversion_type in CONVERSION_TYPES:
        next_seeds = list()
        the_map = mp[conversion_type]
        for dest, source, length in the_map:
            kept_seeds = list()
            for seed in seeds:
                seed_low, seed_high = seed
                source_low, source_high = source, source + length
                iv1 = seed_low, min(seed_high, source_low)
                iv2 = max(source_low, seed_low), min(source_high, seed_high)
                iv3 = max(source_high, seed_low), seed_high
                if iv1[1] > iv1[0]:
                    kept_seeds.append(iv1)
                if iv2[1] > iv2[0]:
                    next_seeds.append((iv2[0] - source + dest, iv2[1] - source + dest))
                if iv3[1] > iv3[0]:
                    kept_seeds.append(iv3)
            seeds = kept_seeds
        seeds = kept_seeds + next_seeds
    return min(seed[0] for seed in seeds)


def part1(inp):
    mp = parse(inp)
    return min(convert(seed, mp) for seed in mp["seeds"])


def part2(inp):
    mp = parse(inp)
    mn = float('inf')
    for lo, ln in zip(mp["seeds"][0::2], mp["seeds"][1::2]):
        mn = min(convert_ranges((lo, lo + ln), mp), mn)
    return mn


def test_1_1():
    assert part1("""seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4""") == 35


def test_2_1():
    assert part2("""seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4""") == 46


def main(inp):
    print("Part1:", part1(inp.strip()))
    print("Part2:", part2(inp.strip()))


if __name__ == "__main__":
    prep = PrepareAoc(2023, 5)
    main(prep.get_content())