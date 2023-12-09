from aoc_prepare import PrepareAoc

def parse(inp):
    for line in inp.splitlines():
        yield [int(i) for i in line.split()]


def extrapolate1(l):
    ll = [y - x for x, y in zip(l[0::1], l[1::1])]
    if all((x == 0 for x in ll)):
        return l[-1]
    return extrapolate1(ll) + l[-1]


def part1(inp):
    return sum((extrapolate1(values) for values in parse(inp)))


def extrapolate2(l):
    ll = [y - x for x, y in zip(l[0::1], l[1::1])]
    if all((x == 0 for x in ll)):
        return l[-1]
    return l[0] - extrapolate2(ll)


def part2(inp):
    return sum((extrapolate2(values) for values in parse(inp)))


def test_1_1():
    assert 114 == part1("""0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45""")



def test_2_1():
    assert 2 == part2("""0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45""")


def main(inp):
    print("Part1:", part1(inp.strip()))
    print("Part2:", part2(inp.strip()))


if __name__ == "__main__":
    prep = PrepareAoc(2023, 9)
    main(prep.get_content())