from aoc_prepare import PrepareAoc
from math import gcd


def parse(inp):
    d = dict()
    for line in inp.splitlines():
        if line == "":
            continue
        if '=' not in line:
            instr = line.strip()
            continue
        start, _, left, right = line.split()
        left = left[1:-1]
        right = right[:-1]
        d[start] = {"L":left, "R":right}
    return d, instr


def part1(inp):
    d, instr = parse(inp)
    i = 0
    current = "AAA"
    while True:
        current = d[current][instr[i % len(instr)]]
        i += 1
        if current == "ZZZ":
            break
    return i


def part2(inp):
    d, instr = parse(inp)
    result = 1
    for start_node in d:
        if start_node[-1] != "A":
            continue
        current = start_node
        i = 0
        while True:
            current = d[current][instr[i % len(instr)]]
            i += 1
            if current[-1] == "Z":
                result = result * i // gcd(result, i)
                break
    return result


def test_1_1():
    assert 2 == part1("""RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)""")


def test_1_2():
    assert 6 == part1("""LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)""")


def test_2_1():
    assert 6 == part2("""LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)""")


def main(inp):
    print("Part1:", part1(inp.strip()))
    print("Part2:", part2(inp.strip()))


if __name__ == "__main__":
    prep = PrepareAoc(2023, 8)
    main(prep.get_content())