from aoc_prepare import PrepareAoc

from position import Pos2D
from collections import namedtuple, deque, Counter
from prio_queue import PrioQueue


def parse(inp):
    d = list()
    for _, line in enumerate(inp.splitlines()):
        part1, _, part2 = line.partition('~')
        end1 = tuple(map(int, part1.split(",")))
        end2 = tuple(map(int, part2.split(",")))
        d.append((end1, end2))
    return d


def resting_bricks(bricks):
    sorted_bricks = sorted(bricks, key=lambda x: (x[0][2], x[1][2]))
    brick_map = dict()
    resting_bricks = list()
    for brick_idx, brick in enumerate(sorted_bricks):
        (x0, y0, z0), (x1, y1, z1) = brick
        high_z = 0
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                if (x, y) not in brick_map:
                    brick_map[x, y] = dict()
                else:
                    high_z = max(high_z, max(brick_map[x, y].keys()))
        delta_z = z0 - high_z - 1
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                for z in range(z0, z1 + 1):
                    brick_map[x, y][z - delta_z] = brick_idx
        resting_bricks.append(((x0, y0, z0 - delta_z), (x1, y1, z1 - delta_z)))
    return resting_bricks, brick_map

def part1(inp):
    bricks = parse(inp)
    fallen_bricks, brick_map = resting_bricks(bricks)
    supporting_bricks = set(range(len(fallen_bricks)))
    for brick in fallen_bricks:
        (x0, y0, z0), (x1, y1, _) = brick
        supporters = set()
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                for z, brick_idx in brick_map[x, y].items():
                    if z == z0 - 1:
                        supporters.add(brick_idx)
        if len(supporters) == 1:
            supporting_bricks = supporting_bricks - supporters
    return len(supporting_bricks)
            

def part2(inp):
    bricks = parse(inp)
    bricks.sort(key=lambda x: (x[0][2], x[1][2]))
    fallen_bricks, brick_map = resting_bricks(bricks)
    supporters_for_brick = dict()
    for brick_idx, brick in enumerate(fallen_bricks):
        (x0, y0, z0), (x1, y1, _) = brick
        supporters = set()
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                for z, supporter_idx in brick_map[x, y].items():
                    if z == z0 - 1:
                        supporters.add(supporter_idx)
        supporters_for_brick[brick_idx] = supporters
    total_falling = 0
    for falling_brick_idx, _ in enumerate(fallen_bricks):
        falling_bricks = set()
        falling_bricks.add(falling_brick_idx)
        for brick_idx2, _ in enumerate(fallen_bricks):
            if len(supporters_for_brick[brick_idx2]) > 0 and supporters_for_brick[brick_idx2] <= falling_bricks:
                falling_bricks.add(brick_idx2)
        total_falling += (len(falling_bricks) - 1)
    return total_falling


def test_1_1():
    assert 5 == part1("""1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9""")

def test_2_1():
    assert 7 == part2("""1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9""")


def main(inp):
    print("Part1:", part1(inp.strip()))
    print("Part2:", part2(inp.strip()))


if __name__ == "__main__":
    prep = PrepareAoc(2023, 22)
    main(prep.get_content())