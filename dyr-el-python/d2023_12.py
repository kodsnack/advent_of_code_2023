from aoc_prepare import PrepareAoc

def parse(inp):
    result = list()
    for lidx, line in enumerate(inp.splitlines()):
        springs, numbers = line.split()
        numbers = tuple(map(int, numbers.split(',')))
        yield numbers, springs


def removeDots(springs):
    for idx, c in enumerate(springs):
        if c != ".":
            return springs[idx:]
    return ""


def removeHash(springs, n):
    if len(springs) >= n and springs[:n].count(".") == 0:
        if len(springs) == n:
            return ""
        if springs[n] != "#":
            return springs[n+1:]
    return None

cache = dict()
def matches(numbers, springs):
    springs = removeDots(springs)
    if (numbers, springs) in cache:
        return cache[numbers, springs]
    if len(numbers) == 0 and springs.count("#") == 0:
        result = 1
    elif len(numbers) == 0:
        result = 0
    elif len(springs) == 0:
        result = 0
    elif springs[0] == "#":
        new_springs = removeHash(springs, numbers[0])
        if new_springs is None:
            result = 0
        else:
            result = matches(numbers[1:], new_springs)
    else:
        new_springs = removeHash(springs, numbers[0])
        if new_springs is None:
            result = 0
        else:
            result = matches(numbers[1:], new_springs)
        result += matches(numbers, springs[1:])
    cache[numbers, springs] = result
    return result

def part1(inp):
    return sum((matches(numbers, springs)
                for numbers, springs in parse(inp)))

def part2(inp):
    return sum((matches(numbers * 5, '?'.join([springs] * 5))
                for numbers, springs in parse(inp)))


def test_1_1():
    assert 21 == part1("""???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""")


def test_2_1():
    assert 1 == part2("""???.### 1,1,3""")


def test_2_2():
    assert 16384 == part2(""".??..??...?##. 1,1,3""")


def test_2_3():
    assert 1 == part2("""?#?#?#?#?#?#?#? 1,3,1,6""")


def test_2_4():
    assert 16 == part2("""????.#...#... 4,1,1""")


def test_2_5():
    assert 2500 == part2("""????.######..#####. 1,6,5""")


def test_2_6():
    assert 506250 == part2("""?###???????? 3,2,1""")


def main(inp):
    print("Part1:", part1(inp.strip()))
    print("Part2:", part2(inp.strip()))


if __name__ == "__main__":
    prep = PrepareAoc(2023, 12)
    main(prep.get_content())
