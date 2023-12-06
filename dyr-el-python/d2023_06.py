from aoc_prepare import PrepareAoc


def get_all_parsing(parsefunc, inp):
    for part in inp.split():
        try:
            yield parsefunc(part)
        except:
            pass


def parse1(inp):
    times, dists = inp.splitlines()
    return get_all_parsing(int, times), get_all_parsing(int, dists)


def parse2(inp):
    return map(int, (''.join(c 
                             for c in line 
                             if c.isdigit())
                     for line in inp.splitlines()))


def boundaries(time, dist):
    low_limit = ceil(time / 2 - sqrt(time * time / 4 - dist))
    if low_limit == time / 2 - sqrt(time * time / 4 - dist):
        low_limit += 1
    high_limit = floor(time / 2 + sqrt(time * time / 4 - dist))
    if high_limit == time / 2 + sqrt(time * time / 4 - dist):
        high_limit -= 1
    return high_limit - low_limit + 1


def part1(inp):
    times, dists = parse1(inp)
    result = 1
    for time, dist in zip(times, dists):
        result *= boundaries(time, dist)
    return result


from math import sqrt, floor, ceil
def part2(inp):
    time, dist = parse2(inp)
    return boundaries(time, dist)


def test_1_1():
    assert 288 == part1("""Time:      7  15   30
Distance:  9  40  200""")


def test_2_1():
    assert 71503 == part2("""Time:      7  15   30
Distance:  9  40  200""")


def main(inp):
    print("Part1:", part1(inp.strip()))
    print("Part2:", part2(inp.strip()))


if __name__ == "__main__":
    prep = PrepareAoc(2023, 6)
    main(prep.get_content())