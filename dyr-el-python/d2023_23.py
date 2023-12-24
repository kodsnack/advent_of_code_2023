from aoc_prepare import PrepareAoc

from position import Pos2D
from collections import namedtuple, deque, Counter
from prio_queue import PrioQueue


def parse(inp):
    d = dict()
    for lidx, line in enumerate(inp.splitlines()):
        for cidx, c in enumerate(line):
            d[Pos2D(cidx, lidx)] = c
    return d


def part1(inp):
    mp = parse(inp)
    starting_pos = Pos2D(1, 0)
    d = deque([starting_pos])
    visited = {starting_pos:[starting_pos]}
    while d:
        pos = d.pop()
        for next_pos in (pos.north(), pos.south(), pos.west(), pos.east()):
            if next_pos not in mp:
                continue
            c = mp[next_pos]
            if c == "#":
                continue
            if c == ">":
                npos = next_pos.east()
                steps = 2
            if c == "<":
                npos = next_pos.west()
                steps = 2
            if c == "v":
                npos = next_pos.south()
                steps = 2
            if c == "^":
                npos = next_pos.north()
                steps = 2
            if c == ".":
                npos = next_pos
                steps = 1
            if npos in visited:
                if len(visited[pos]) + steps > len(visited[npos]) and npos not in visited[pos]:
                    if npos != next_pos:
                        visited[next_pos] = visited[pos] + [next_pos]
                        visited[npos] = visited[pos] + [next_pos, npos]
                    else:
                        visited[npos] = visited[pos] + [npos]
                    d.append(npos)
            else:
                if npos != next_pos:
                    visited[next_pos] = visited[pos] + [next_pos]
                    visited[npos] = visited[pos] + [next_pos, npos]
                else:
                    visited[npos] = visited[pos] + [npos]
                d.append(npos)
    xmax = max((pos.x for pos in mp))
    ymax = max((pos.y for pos in mp))
    for pos, path in visited.items():
        if pos.y == ymax:
            the_path = visited[pos]
    return len(the_path) - 1

mmax = 0
def recurse(pathing, so_far, goal, dist=0):
    global mmax
    current_pos = so_far[-1]
    if goal == current_pos:
        if dist > mmax:
            mmax = dist
        return dist
    possibles = pathing[current_pos]
    max_dist = 0
    for poss in possibles:
        if poss in so_far:
            continue
        rest_dist = recurse(pathing, so_far + [poss], goal, dist + len(pathing[current_pos][poss][0]))
        if rest_dist > max_dist:
            max_dist = rest_dist
    return max_dist


def part2(inp):
    mp = parse(inp)
    starting_pos = Pos2D(1, 0)
    xmax = max((pos.x for pos in mp))
    ymax = max((pos.y for pos in mp))
    nodes = set()
    for x in range(xmax+1):
        if mp[Pos2D(x, 0)] == ".":
            nodes.add(Pos2D(x, 0))
            real_start = Pos2D(x, 0)
        if mp[Pos2D(x, ymax)] == ".":
            nodes.add(Pos2D(x, ymax))
            real_end = Pos2D(x, ymax)
    for pos in mp:
        if mp[pos] == "#":
            continue
        exits = 0
        for next_pos in (pos.north(), pos.south(), pos.west(), pos.east()):
            if next_pos in mp and mp[next_pos] != "#":
                exits += 1
        if exits > 2:
            nodes.add(pos)
    pathing = dict()
    for start in nodes:
        d = deque()
        d.append([start])
        while d:
            path = d.popleft()
            pos = path[-1]
            for next_pos in (pos.north(), pos.south(), pos.east(), pos.west()):
                if next_pos not in mp or mp[next_pos] == "#":
                    continue
                if next_pos in path:
                    continue
                if next_pos in nodes:
                    if start not in pathing:
                        pathing[start] = dict()
                    if next_pos not in pathing[start]:
                        pathing[start][next_pos] = list()
                    pathing[start][next_pos].append(path[1:] + [next_pos])
                else:
                    d.append(path + [next_pos])
    return recurse(pathing, [real_start], real_end)


def test_1_1():
    assert 94 == part1("""#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#""")


def test_2_1():
    assert 154 == part2("""#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#""")


def main(inp):
    print("Part1:", part1(inp.strip()))
    print("Part2:", part2(inp.strip()))


if __name__ == "__main__":
    prep = PrepareAoc(2023, 23)
    main(prep.get_content())