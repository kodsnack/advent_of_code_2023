from aoc_prepare import PrepareAoc

def parse(inp):
    result = dict()
    maxx = 0
    maxy = 0
    for lidx, line in enumerate(inp.splitlines()):
        maxy = max(lidx, maxy)
        for cidx, c in enumerate(line):
            maxx = max(cidx, maxx)
            if c != '.':
                result[lidx, cidx] = c
    
    return result, maxy, maxx


def tilt_north(d, limit=0):
    dd = dict()
    changed = True
    while changed:
        changed = False
        for (y, x), c in d.items():
            if y > limit and c == 'O' and (y-1, x) not in d:
                dd[y-1, x] = d[y, x]
                changed = True
            else:
                dd[y, x] = d[y, x]
        d = dd
        dd = dict()
    return d

def tilt_west(d, limit=0):
    dd = dict()
    changed = True
    while changed:
        changed = False
        for (y, x), c in d.items():
            if x > limit and c == 'O' and (y, x - 1) not in d:
                dd[y, x - 1] = d[y, x]
                changed = True
            else:
                dd[y, x] = d[y, x]
        d = dd
        dd = dict()
    return d

def tilt_south(d, limit):
    dd = dict()
    changed = True
    while changed:
        changed = False
        for (y, x), c in d.items():
            if y < limit and c == 'O' and (y+1, x) not in d:
                dd[y+1, x] = d[y, x]
                changed = True
            else:
                dd[y, x] = d[y, x]
        d = dd
        dd = dict()
    return d

def tilt_east(d, limit):
    dd = dict()
    changed = True
    while changed:
        changed = False
        for (y, x), c in d.items():
            if x < limit and c == 'O' and (y, x + 1) not in d:
                dd[y, x + 1] = d[y, x]
                changed = True
            else:
                dd[y, x] = d[y, x]
        d = dd
        dd = dict()
    return d

def weigh(d):
    sm = 0
    maxy = max((y for y, _ in d))
    for (y, x), c in d.items():
        if c == 'O':
            sm += (maxy + 1 - y)
    return sm

def part1(inp):
    result, _, _ = parse(inp)
    result = tilt_north(result)
    return weigh(result)

def board_key(d, maxy, maxx):
    return frozenset((y, x) for y, x in d if d[y, x] == 'O')

def part2(inp):
    result, maxy, maxx = parse(inp)
    cache = dict()
    i = 0
    found_cycle = False
    while i < 1000000000:
        result = tilt_north(result, 0)
        result = tilt_west(result, 0)
        result = tilt_south(result, maxy)
        result = tilt_east(result, maxx)
        i += 1
        key = board_key(result, maxy, maxx)
        if not found_cycle and key in cache:
            cycle = i - cache[key]
            i = i + ((1000000000 - i) // cycle) * cycle
            found_cycle = True
        else:
            cache[key] = i
    return weigh(result)

def test_1_1():
    assert 136 == part1("""O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....""")


def test_1_2():
    assert 64 == part2("""O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....""")

def main(inp):
    print("Part1:", part1(inp.strip()))
    print("Part2:", part2(inp.strip()))


if __name__ == "__main__":
    prep = PrepareAoc(2023, 14)
    main(prep.get_content())