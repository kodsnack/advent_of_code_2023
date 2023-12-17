from aoc_prepare import PrepareAoc
import sys

def parse(inp):
    board = [c for c in inp if c in "#O."]
    maxx = len(inp.splitlines()[0])
    maxy = len(inp.splitlines())
    return board, maxy, maxx

def print_board(a, maxy, maxx):
    for idx, c in enumerate(a):
        print(c, end="")
        if (idx % maxx) == maxx - 1:
            print()

def tilt_n(a, maxy, maxx):
    for x in range(maxx):
        slot = x
        for y in range(maxy):
            pos = y * maxx + x
            c = a[pos]
            if c == "#":
                slot = pos + maxx
            elif c == "O":
                a[slot] = "O"
                if slot != pos:
                    a[pos] = "."
                slot += maxx

def tilt_s(a, maxy, maxx):
    for x in range(maxx):
        slot = maxx * (maxy - 1) + x
        for y in range(maxy - 1, -1, -1):
            pos = y * maxx + x
            c = a[pos]
            if c == "#":
                slot = pos - maxx
            elif c == "O":
                a[slot] = "O"
                if slot != pos:
                    a[pos] = "."
                slot -= maxx

def tilt_w(a, maxy, maxx):
    for y in range(maxy):
        slot = maxx * y
        for x in range(maxx):
            pos = y * maxx + x
            c = a[pos]
            if c == "#":
                slot = pos + 1
            elif c == "O":
                a[slot] = "O"
                if slot != pos:
                    a[pos] = "."
                slot += 1

def tilt_e(a, maxy, maxx):
    for y in range(maxy):
        slot = maxx * (y + 1) - 1
        for x in range(maxx - 1, -1 , -1):
            pos = y * maxx + x
            c = a[pos]
            if c == "#":
                slot = pos - 1
            elif c == "O":
                a[slot] = "O"
                if slot != pos:
                    a[pos] = "."
                slot -= 1

def weigh(a, maxy, maxx):
    return sum(((maxy - idx // maxx) for idx, c in enumerate(a) if c == "O"))

def part1(inp):
    a, maxy, maxx = parse(inp)
    tilt_n(a, maxy, maxx)
    return weigh(a, maxy, maxx)

def part2(inp):
    result, maxy, maxx = parse(inp)
    cache = dict()
    i = 0
    found_cycle = False
    while i < 1000000000:
        tilt_n(result, maxy, maxx)
        tilt_w(result, maxy, maxx)
        tilt_s(result, maxy, maxx)
        tilt_e(result, maxy, maxx)
        i += 1
        key = "".join(result)
        if not found_cycle and key in cache:
            cycle = i - cache[key]
            i = i + ((1000000000 - i) // cycle) * cycle
            found_cycle = True
        else:
            cache[key] = i
    return weigh(result, maxy, maxx)

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

from timeit import Timer
def main_timer(inp):
    timer = Timer(stmt='part1(inp.strip())', setup=f"inp='''{inp}'''", globals=globals())
    iterations, time = timer.autorange()
    print("average time for part 1 =", time/iterations)
    timer = Timer(stmt='part2(inp.strip())', setup=f"inp='''{inp}'''", globals=globals())
    iterations, time = timer.autorange()
    print("average time for part 2 =", time/iterations)

import cProfile
def main_profile(inp):
    cProfile.runctx('part1(inp.strip())', globals=globals(), locals={'inp':inp})
    cProfile.runctx('part2(inp.strip())', globals=globals(), locals={'inp':inp})

if __name__ == "__main__":
    prep = PrepareAoc(2023, 14)
    if "skip" not in sys.argv:
        main(prep.get_content())
    if "time" in sys.argv:
        main_timer(prep.get_content())
    if "profile" in sys.argv:
        main_profile(prep.get_content())