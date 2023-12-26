from aoc_prepare import PrepareAoc

from position import Pos2D
from collections import namedtuple, deque, Counter
from prio_queue import PrioQueue


def parse(inp):
    d = dict()
    start = None
    for lidx, line in enumerate(inp.splitlines()):
        for cidx, c in enumerate(line):
            if c == '.':
                d[Pos2D(cidx, lidx)] = c
            elif c == 'S':
                d[Pos2D(cidx, lidx)] = c
                start = Pos2D(cidx, lidx)
    return d, start


def step_sand(sand_map, positions, x_size, y_size):
    new_positions = set()
    for position in positions:
        for new_position in (position.north(), position.south(), position.west(), position.east()):
            mod_position = Pos2D(new_position.x % x_size, new_position.y % y_size)
            if mod_position in sand_map:
                new_positions.add(new_position)
    return new_positions


def color_sand(sand_map, start, max_steps, x_size, y_size):
    step_count = {start: 0}
    remaining = deque([start])
    while remaining:
        position = remaining.popleft()
        if step_count[position] == max_steps:
            return step_count
        for new_position in (position.north(), position.south(), position.west(), position.east()):
            if new_position in step_count:
                continue
            mod_position = Pos2D(new_position.x % x_size, new_position.y % y_size)
            if mod_position in sand_map:
                step_count[new_position] = step_count[position] + 1
                remaining.append(new_position)

def part1(inp, steps):
    sand_map, start_position = parse(inp)
    maxx, maxy = max((x.x for x in sand_map)), max((x.y for x in sand_map))
    x_size, y_size = maxx + 1, maxy + 1
    step_count = color_sand(sand_map, start_position, steps, x_size, y_size)
    return sum((1 - steps % 2 for steps in step_count.values()))


def part2(inp, steps):
    sand_map, start_position = parse(inp)
    maxx, maxy = max((x.x for x in sand_map)), max((x.y for x in sand_map))
    x_size, y_size = maxx + 1, maxy + 1
    step_count = color_sand(sand_map, start_position, x_size * 2 + x_size // 2, x_size, y_size)
    mp = dict()
    for pos, count in step_count.items():
        mp[pos.x // x_size, pos.y // y_size] = mp.get((pos.x // x_size, pos.y // y_size), 0) + (count % 2)
    higher = (steps - x_size // 2) // x_size
    lesser = higher - 1
    return (higher ** 2 * mp[0, -1] + lesser ** 2 * mp[0, 0] + 
            higher * (mp[1, -2] + mp[-1, -2] + mp[-1, 2] + mp[1, 2]) +
            lesser * (mp[1, -1] + mp[-1, -1] + mp[1, 1] + mp[-1, 1]) +
            mp[2, 0] + mp[-2, 0] + mp[0, -2] + mp[0, 2]) 


def test_1_1():
    assert 16 == part1("""...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........""", 6)


def test_1_2():
    assert 50 == part1("""...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........""", 10)

def test_1_3():
    assert 1594 == part1("""...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........""", 50)

def test_1_4():
    assert 6536 == part1("""...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........""", 100)

def test_1_5():
    assert 167004 == part1("""...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........""", 500)


def main(inp):
    print("Part1:", part1(inp.strip(), 64))
    print("Part2:", part2(inp.strip(), 26501365))


if __name__ == "__main__":
    prep = PrepareAoc(2023, 21)
    main(prep.get_content())