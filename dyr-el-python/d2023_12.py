from aoc_prepare import PrepareAoc

def parse(inp):
    result = list()
    for lidx, line in enumerate(inp.splitlines()):
        springs, numbers = line.split()
        numbers = list(map(int, numbers.split(',')))
        springs = list(springs)
        yield numbers, springs


def matches_old(numbers, springs):
    nr = springs.count("?")
    result = 0
    print(nr)
    for i in range(2 ** nr):
        ii = i
        l = list()
        for j in range(nr):
            if ii % 2 == 0:
                l.append('.')
            else:
                l.append('#')
            ii //= 2
        l = ''.join(l)
        ll = list()
        for c in springs:
            if c == "?":
                ll.append(l[0])
                l = l[1:]
            else:
                ll.append(c)
        lll = list()
        current = 0
        for c in ll:
            if c == ".":
                if current > 0:
                    lll.append(current)
                    current = 0
            if c == "#":
                current += 1
        if current > 0:
            lll.append(current)
        if numbers == lll:
            result += 1
    print(result)
    return result

def removeDots(springs):
    while len(springs) > 0 and springs[0] == '.':
        springs = springs[1:]
    return springs

def removeSprings(springs, n):
    for _ in range(n):
        if len(springs) == 0:
            return None
        if springs[0] == '.':
            return None
        springs = springs[1:]
    if len(springs) == 0:
        return springs
    if springs[0] == '#':
        return None
    if springs[0] == '?':
        return springs[1:]
    return springs

def matches(numbers, springs):
    print(f"matches({numbers=}, {springs=})")
    if len(numbers) == 0 and springs.count('#') == 0:
        print("<- 1")
        return 1
    if len(numbers) == 0:
        print("<- 0")
        return 0
    if len(springs) == 0:
        print("<- 0")
        return 0
    if springs[0] == ".":
        result = matches(numbers, springs[1:])
        print("<-", result)
        return result
    if springs[0] == "#":
        new_springs = removeSprings(springs, numbers[0])
        if new_springs is None:
            print("<- 0")
            return 0
        result = matches(numbers[1:], new_springs)
        print("<-", result)
        return result
    result = matches(numbers, springs[1:])
    new_springs = removeSprings(springs, numbers[0])
    if new_springs is not None:
        result += matches(numbers[1:], new_springs)
    print("<-", result)
    return result


def part1(inp):
    sm = 0
    for numbers, springs in parse(inp):
        sm += matches(numbers, springs)
    return sm

def part2(inp):
    sm = 0
    for numbers, springs in parse(inp):
        for p in (('.', '.', '.', '.'),
                  ('.', '.', '.', '#'),
                  ('.', '.', '#', '.'),
                  ('.', '.', '#', '#'),
                  ('.', '#', '.', '.'),
                  ('.', '#', '.', '#'),
                  ('.', '#', '#', '.'),
                  ('.', '#', '#', '#'),
                  ('#', '.', '.', '.'),
                  ('#', '.', '.', '#'),
                  ('#', '.', '#', '.'),
                  ('#', '.', '#', '#'),
                  ('#', '#', '.', '.'),
                  ('#', '#', '.', '#'),
                  ('#', '#', '#', '.'),
                  ('#', '#', '#', '#')):
            nn = numbers * 5
            spr = springs + [p[0]] + springs + [p[1]] + springs + [p[2]] + springs + [p[3]]
            print(nn, spr)
            sm += matches(nn, spr)
    return sm


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
    assert 1 == part2(""".??..??...?##. 1,1,3""")

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