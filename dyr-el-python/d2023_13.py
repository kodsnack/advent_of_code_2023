from aoc_prepare import PrepareAoc
from collections import deque, Counter


def parse(inp):
    result = list()
    for bidx, board in enumerate(inp.split('\n\n')):
        b = dict()
        for lidx, line in enumerate(board.splitlines()):
            for cidx, c in enumerate(line):
                b[lidx, cidx] = c
        result.append(b)
    return result


def find_vertical(b):
    d = dict()
    ymax = max([c[0] for c in b])
    xmax = max([c[1] for c in b])
    for symmetry_idx in range(1, xmax + 1):
        smudges = 0
        for y in range(ymax + 1):
            for x in range(min(symmetry_idx, xmax - symmetry_idx + 1)):
                if b[y, symmetry_idx + x] != b[y, symmetry_idx - x - 1]:
                    smudges += 1
        d[smudges] = symmetry_idx
    return d


def find_horizontal(b):
    d = dict()
    ymax = max([c[0] for c in b])
    xmax = max([c[1] for c in b])
    for symmetry_idx in range(1, ymax + 1):
        smudges = 0
        for y in range(min(symmetry_idx, ymax - symmetry_idx + 1)):
            for x in range(xmax + 1):
                if b[symmetry_idx + y, x] != b[symmetry_idx - y - 1, x]:
                    smudges += 1
        d[smudges] = symmetry_idx
    return d


def part1(inp):
    boards = parse(inp)
    result = 0
    for board in boards:
        v = find_vertical(board)
        if 0 in v:
            result += v[0]
            continue
        h = find_horizontal(board)
        if 0 in h:
            result += (h[0] * 100)
    return result


def part2(inp):
    boards = parse(inp)
    result = 0
    for board in boards:
        v = find_vertical(board)
        if 1 in v:
            result += v[1]
            continue
        h = find_horizontal(board)
        if 1 in h:
            result += (h[1] * 100)
    return result


def test_1_1():
    assert 405 == part1("""#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#""")


def test_1_2():
    assert 400 == part2("""#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#""")


def main(inp):
    print("Part1:", part1(inp.strip()))
    print("Part2:", part2(inp.strip()))


if __name__ == "__main__":
    prep = PrepareAoc(2023, 13)
    main(prep.get_content())