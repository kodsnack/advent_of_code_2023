from aoc_prepare import PrepareAoc
from position import Pos2D
from collections import namedtuple, deque, Counter
from prio_queue import PrioQueue


def parse(inp):
    result = dict()
    for lidx, line in enumerate(inp.splitlines()):
        direction, number,color = line.split()
        number = int(number)
        color = int(color[2:-1], 16)
        yield direction, number, color


def parse2(inp):
    for lidx, line in enumerate(inp.splitlines()):
        _, _, color = line.split()
        direction = int(color[-2])
        length = int(color[2:-2], 16)
        yield direction, length


def flood_fill(trenches, pos, color, minx, maxx, miny, maxy):
    d = deque()
    d.append(pos)
    while d:
        pos = d.popleft()
        if pos in trenches:
            continue
        trenches[pos] = color
        for npos in (pos.north(), pos.south(), pos.west(), pos.east()):
            if npos.y < miny or npos.x < minx or npos.x > maxx or npos.y > maxy:
                continue
            d.append(npos)


def fill_outside(trenches):
    maxx = max((pos.x for pos in trenches))
    maxy = max((pos.y for pos in trenches))
    minx = min((pos.x for pos in trenches))
    miny = min((pos.y for pos in trenches))
    for x in range(minx, maxx + 1):
        pos = Pos2D(x, miny)
        if pos not in trenches:
            flood_fill(trenches, pos, -1, minx, maxx, miny, maxy)
        pos = Pos2D(x, maxy)
        if pos not in trenches:
            flood_fill(trenches, pos, -1, minx, maxx, miny, maxy)
    for y in range(miny, maxy + 1):
        pos = Pos2D(minx, y)
        if pos not in trenches:
            flood_fill(trenches, pos, -1, minx, maxx, miny, maxy)
        pos = Pos2D(maxx, y)
        if pos not in trenches:
            flood_fill(trenches, pos, -1, minx, maxx, miny, maxy)

def color_trenches(trenches, segments):
    pos = Pos2D(0, 0)
    deltas = {"U": Pos2D(0, -1), "D": Pos2D(0, 1), "L": Pos2D(-1, 0), "R": Pos2D(1, 0)}
    for dir, number, color in segments:
        for _ in range(number):
            pos = pos + deltas[dir]
            trenches[pos] = color


def part1(inp):
    trenches = dict()
    pos = Pos2D(0, 0)
    color_trenches(trenches, parse(inp))
    fill_outside(trenches)
    maxx = max((pos.x for pos in trenches))
    maxy = max((pos.y for pos in trenches))
    minx = min((pos.x for pos in trenches))
    miny = min((pos.y for pos in trenches))
    return (maxx - minx + 1) * (maxy - miny + 1) - sum((trench < 0 for trench in trenches.values()))


def find_verticals(actions):
    result = list()
    dirs = {0: Pos2D(1, 0), 1: Pos2D(0, 1), 2: Pos2D(-1, 0), 3: Pos2D(0, -1)}
    pos = Pos2D(0, 0)
    for direction, length in actions:
        next_pos = dirs[direction] * length + pos
        if direction in (1, 3):
            result.append((pos, next_pos))
        pos = next_pos
    result.sort(key=lambda v:(v[0].x, min(v[0].y, v[1].y)))
    return result


def area_for_horizontal_lines(verticals, v_ypos):
    area = 0
    for y in v_ypos:
        state = "outside"
        for vertical in verticals:
            vymin, vymax = min(vertical[0].y, vertical[1].y), max(vertical[0].y, vertical[1].y)
            if state == "outside":
                if y == vymin:
                    state = "below"
                    startx = vertical[1].x
                elif y == vymax:
                    state = "above"
                    startx = vertical[1].x
                elif vymin < y < vymax:
                    state = "inside"
                    startx = vertical[1].x
            elif state == "inside":
                if y == vymin:
                    state = "above"
                elif y == vymax:
                    state = "below"
                elif vymin < y < vymax:
                    state = "outside"
                    area += (vertical[1].x - startx + 1)
            elif state == "above":
                if y == vymin:
                    state = "inside"
                elif y == vymax:
                    state = "outside"
                    area += (vertical[1].x - startx + 1)
            elif state == "below":
                if y == vymin:
                    state = "outside"
                    area += (vertical[1].x - startx + 1)
                elif y == vymax:
                    state = "inside"
    return area


def area_for_vertical_blocks(verticals, h_ypos):
    ongoing = dict()
    area = 0
    for y in h_ypos:
        state = "outside"
        for vertical in verticals:
            vymin, vymax = min(vertical[0].y, vertical[1].y), max(vertical[0].y, vertical[1].y)
            if y <= vymin or y >= vymax:
                continue
            if state == "outside":
                state = "inside"
                xstart = vertical[0].x
                continue
            xend = vertical[0].x
            if (xstart, xend) in ongoing:
                area += (xend - xstart + 1) * (y - ongoing[(xstart, xend)] + 1)
                del ongoing[(xstart, xend)]
            else:
                ongoing[(xstart, xend)] = y
            state = "outside"
    return area


def part2(inp):
    verticals = find_verticals(parse2(inp))
    v_ypos = sorted(set([vertical[0].y for vertical in verticals] +
                        [vertical[1].y for vertical in verticals]))
    ymin, ymax = v_ypos[0], v_ypos[-1]
    h_ypos = sorted(set([y+1 for y in v_ypos] + [y-1 for y in v_ypos]) - set(v_ypos))[1:-1]
    area = (area_for_horizontal_lines(verticals, v_ypos)
            + area_for_vertical_blocks(verticals, h_ypos))
    return area


def test_1_1():
    assert 62 == part1("""R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)""")


def test_2_1():
    assert 952408144115 == part2("""R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)""")


def main(inp):
    print("Part1:", part1(inp.strip()))
    print("Part2:", part2(inp.strip()))


if __name__ == "__main__":
    prep = PrepareAoc(2023, 18)
    main(prep.get_content())
