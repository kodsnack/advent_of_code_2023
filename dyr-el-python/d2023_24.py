from aoc_prepare import PrepareAoc

from position import Pos2D
from collections import namedtuple, deque, Counter
from prio_queue import PrioQueue
import z3

def parse(inp):
    d = dict()
    for lidx, line in enumerate(inp.splitlines()):
        p, _,  v = line.partition(' @ ')
        px, py, pz = map(int, p.split(', '))
        vx, vy, vz = map(int, v.split(', '))
        yield (px, py, pz), (vx, vy, vz)


def part1(inp, min_p, max_p):
    hs = list(parse(inp))
    count = 0
    for hs1 in hs:
        (hs1px, hs1py, _), (hs1vx, hs1vy, _) = hs1
        for hs2 in hs:
            (hs2px, hs2py, _), (hs2vx, hs2vy, _) = hs2
            # -> hs1px + t1 * hs1vx == hs2px + t2 * hs2vx
            # t1 = (hs2px + t2 * hs2vx - hs1px) / hs1vx
            # -> hs1py + t1 * hs1vy == hs2py + t2 * hs2vy
            # hs1py + (hs2px + t2 * hs2vx - hs1px) / hs1vx * hs1vy == hs2py + t2 * hs2vy
            # (hs2px + t2 * hs2vx - hs1px) / hs1vx * hs1vy - t2 * hs2vy == (hs2py - hs1py)
            # (hs2px - hs1px) * hs1vy / hs1vx + t2 * (hs2vx * hs1vy - hs2vy * hs1vx) / hs1vx ==  (hs2py - hs1py)
            # t2 * (hs2vx * hs1vy - hs2vy * hs1vx) / hs1vx == (hs2py - hs1py) - (hs2px - hs1px) * hs1vy / hs1vx
            if ((hs2vx * hs1vy - hs2vy * hs1vx) / hs1vx) == 0:
                continue
            t2  = ((hs2py - hs1py) - (hs2px - hs1px) * hs1vy / hs1vx) / ((hs2vx * hs1vy - hs2vy * hs1vx) / hs1vx)
            t1  = ((hs1py - hs2py) - (hs1px - hs2px) * hs2vy / hs2vx) / ((hs1vx * hs2vy - hs1vy * hs2vx) / hs2vx)
            if t2 < 0 or t1 < 0:
                continue
            crx, cry = hs1px + t1 * hs1vx, hs1py + t1 * hs1vy
            if min_p > crx or max_p < crx or min_p > cry or max_p < cry:
                continue
            count += 1
    return count // 2

def part2(inp):
    hs = list(parse(inp))
    (p1x, p1y, p1z), (v1x, v1y, v1z) = hs[0]
    (p2x, p2y, p2z), (v2x, v2y, v2z) = hs[1]
    (p3x, p3y, p3z), (v3x, v3y, v3z) = hs[2]
    x, y, z = z3.Int('x'), z3.Int('y'), z3.Int('z')
    vx, vy, vz = z3.Int('vx'), z3.Int('vy'), z3.Int('vz')
    t1, t2, t3 = z3.Int('t1'), z3.Int('t2'), z3.Int('t3')
    s = z3.Solver()
    s.add(x + vx * t1 == p1x + v1x * t1)
    s.add(y + vy * t1 == p1y + v1y * t1)
    s.add(z + vz * t1 == p1z + v1z * t1)
    s.add(x + vx * t2 == p2x + v2x * t2)
    s.add(y + vy * t2 == p2y + v2y * t2)
    s.add(z + vz * t2 == p2z + v2z * t2)
    s.add(x + vx * t3 == p3x + v3x * t3)
    s.add(y + vy * t3 == p3y + v3y * t3)
    s.add(z + vz * t3 == p3z + v3z * t3)
    s.check()
    m = s.model()
    return m[x].as_long() + m[y].as_long() + m[z].as_long()


def test_1_1():
    assert 2 == part1("""19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3""", 7, 27)


def test_2_1():
    assert 47 == part2("""19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3""")


def main(inp):
    print("Part1:", part1(inp.strip(), 200000000000000, 400000000000000))
    print("Part2:", part2(inp.strip()))


if __name__ == "__main__":
    prep = PrepareAoc(2023, 24)
    main(prep.get_content())