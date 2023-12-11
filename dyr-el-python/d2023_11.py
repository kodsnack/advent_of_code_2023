from aoc_prepare import PrepareAoc


def parse(inp):
    d = [(lidx, cidx) 
         for lidx, line in enumerate(inp.splitlines())
         for cidx, c in enumerate(line)
         if c == "#"]
    mx = len(inp.splitlines()[0])
    my = len(inp.splitlines())
    empty_lines = {c for c in range(my + 1)} - {c[0] for c in d}
    empty_cols = {c for c in range(mx + 1)} - {c[1] for c in d}
    return d, empty_lines, empty_cols


def dist(p0, p1, empty_lines, empty_cols, exp=2):
    y0, y1 = min(p0[0], p1[0]), max(p0[0], p1[0])
    x0, x1 = min(p0[1], p1[1]), max(p0[1], p1[1])
    exp_y = len([line for line in empty_lines if y0 < line < y1])
    exp_x = len([cols for cols in empty_cols if x0 < cols < x1])
    return y1-y0 + exp_y * (exp - 1) + x1 - x0 + exp_x * (exp - 1)


def part1(inp, expanse=2):
    d, empty_lines, empty_cols = parse(inp)
    return sum((dist(galaxy1, galaxy2, empty_lines, empty_cols, expanse)
                for galaxy1 in d for galaxy2 in d if galaxy1 < galaxy2))


def part2(inp, expanse=1000000):
    return part1(inp, expanse)


def test_1_1():
    assert 374 == part1("""...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....""")


def test_2_1():
    assert 1030 == part2("""...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....""", expanse=10)


def test_2_2():
    assert 8410 == part2("""...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....""", expanse=100)


def main(inp):
    print("Part1:", part1(inp.strip()))
    print("Part2:", part2(inp.strip()))


if __name__ == "__main__":
    prep = PrepareAoc(2023, 11)
    main(prep.get_content())