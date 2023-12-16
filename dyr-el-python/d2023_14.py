from aoc_prepare import PrepareAoc
from collections import deque

def parse(inp):
    result = {'.':set(), 'O':set(), '#':set()}
    maxx = 0
    maxy = 0
    for lidx, line in enumerate(inp.splitlines()):
        maxy = max(lidx, maxy)
        for cidx, c in enumerate(line.strip()):
            maxx = max(cidx, maxx)
            result[c].add((lidx, cidx))
    return result, maxy + 1, maxx + 1

def tilt(a, dy, dx):
    d = deque(a['O'])
    while d:
        y, x = d.popleft()
        if (y, x) not in a['O']:
            continue
        ny, nx = y+dy, x+dx
        if (ny, nx) in a['.']:
            a['.'].remove((ny, nx))
            a['O'].add((ny, nx))
            a['.'].add((y, x))
            a['O'].remove((y, x))
            d.append((ny, nx))
            oy, ox = y - dy, x - dx
            if (oy, ox) in a['O']:
                d.append((oy, ox))

def weigh(a, maxy, _):
    return sum((maxy - y) for y, _ in a['O'])

def part1(inp):
    result, maxy, maxx = parse(inp)
    tilt(result, -1, 0)
    return weigh(result, maxy, maxx)

def part2(inp):
    result, maxy, maxx = parse(inp)
    cache = dict()
    i = 0
    found_cycle = False
    while i < 1000000000:
        tilt(result, -1, 0)
        tilt(result, 0, -1)
        tilt(result, 1, 0)
        tilt(result, 0, 1)
        i += 1
        key = frozenset(result['O'])
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

if __name__ == "__main__":
    prep = PrepareAoc(2023, 14)
    main(prep.get_content())
    main_timer(prep.get_content())