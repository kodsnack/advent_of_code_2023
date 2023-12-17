from aoc_prepare import PrepareAoc
import sys
from collections import deque

def parse(inp):
    result = dict()
    mxy, mxx = 0, 0
    for lidx, line in enumerate(inp.splitlines()):
        mxy = max(mxy, lidx)
        for cidx, c in enumerate(line):
            result[lidx, cidx] = c
            mxx = max(mxx, cidx)
    return result, mxy, mxx

def energize(grid, sy, sx, sdy, sdx):
    start = deque([(sy, sx, sdy, sdx)])
    visited = set()
    while len(start) > 0:
        y, x, dy, dx = start.popleft()
        if (y, x, dy, dx) in visited:
            continue
        visited.add((y, x, dy, dx))
        c = grid[y, x]
        if (c == '.') or (c == '|' and dy != 0) or (c == '-' and dx != 0):
            dy, dx = (dy, None), (dx, None)
        elif c == '\\':
            dy, dx = (dx, None), (dy, None)
        elif c == '/':
            dy, dx = (-dx, None), (-dy, None)
        elif c == '|':
            dy, dx = (-1, 1), (0, None)
        elif c == '-':
            dy, dx = (0, None), (-1, 1)
        nc = [(y + ddy, x + ddx) 
              for ddy in dy 
              for ddx in dx 
              if ddy is not None and ddx is not None]
        for yy, xx in nc:
            if (yy, xx) not in grid:
                continue
            start.append((yy, xx, yy - y, xx - x))
    return visited

def part1(inp):
    grid, _, _ = parse(inp)
    visited = energize(grid, 0, 0, 0, 1)
    return len({(y, x) for y, x, dy, dx in visited})

def part2(inp):
    maxe = 0
    grid, mxy, mxx = parse(inp)
    for y in range(mxy + 1):
        visited = energize(grid, y, 0, 0, 1)
        maxe = max(maxe, len({(y, x) for y, x, dy, dx in visited}))
        visited = energize(grid, y, mxx, 0, -1)
        maxe = max(maxe, len({(y, x) for y, x, dy, dx in visited}))
    for x in range(mxx + 1):
        visited = energize(grid, 0, x, 1, 0)
        maxe = max(maxe, len({(y, x) for y, x, dy, dx in visited}))
        visited = energize(grid, mxy, x, -1, 0)
        maxe = max(maxe, len({(y, x) for y, x, dy, dx in visited}))
    return maxe


def test_1_1():
    assert 46 == part1(r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....""")


def test_1_2():
    assert 51 == part2(r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....""")


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
    prep = PrepareAoc(2023, 16)
    if "skip" not in sys.argv:
        main(prep.get_content())
    if "time" in sys.argv:
        main_timer(prep.get_content())
    if "profile" in sys.argv:
        main_profile(prep.get_content())