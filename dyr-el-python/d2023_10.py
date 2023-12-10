from aoc_prepare import PrepareAoc
from collections import deque


def parse(inp):
    d = dict()
    xmin, xmax, ymin, ymax = 0, 0, 0, 0
    for lidx, line in enumerate(inp.splitlines()):
        for cidx, ch in enumerate(line):
            l = list()
            if ch in "-J7":
                l.append((lidx, cidx - 1))
            if ch in "-LF":
                l.append((lidx, cidx + 1))
            if ch in "|LJ":
                l.append((lidx - 1, cidx))
            if ch in "|7F":
                l.append((lidx + 1, cidx))
            if ch == "S":
                start_pos = (lidx, cidx)
            d[lidx, cidx] = l
            xmin = min(cidx, xmin)
            xmax = max(cidx, xmax)
            ymin = min(lidx, ymin)
            ymax = max(lidx, ymax)
    l = list()
    for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        y, x = start_pos[0] + dy, start_pos[1] + dx
        if (y, x) in d and start_pos in d[y, x]:
            l.append((y, x))
    d[start_pos] = l
    return d, start_pos, ymin, ymax, xmin, xmax


def find_track(mz, start):
    current = start
    visited = {current}
    while True:
        for next in mz[current]:
            if next not in visited:
                visited.add(next)
                current = next
                break
        else:
            break
    return visited


def part1(inp):
    mz, start, _, _, _, _ = parse(inp)
    visited = find_track(mz, start)
    return len(visited) // 2


def find_left_and_right_set(mz, start, track, backward=False):
    left_set = set()
    right_set = set()
    current = start
    visited = {current}
    while True:
        order = mz[current] if not backward else reversed(mz[current])
        for next in order:
            if next not in visited:
                if next[0] > current[0]:  # stepping south
                    left = current[0], current[1] + 1
                    right = current[0], current[1] - 1
                elif next[0] < current[0]:  # stepping nort
                    left = current[0], current[1] - 1
                    right = current[0], current[1] + 1
                elif next[1] > current[1]:  # stepping east
                    left = current[0] - 1, current[1]
                    right = current[0] + 1, current[1]
                else:  # stepping west
                    left = current[0] + 1, current[1]
                    right = current[0] - 1, current[1]
                if left not in track:
                    left_set.add(left)
                if right not in track:
                    right_set.add(right)
                visited.add(next)
                current = next
                break
        else:
            break
    if not backward:
        return left_set, right_set
    else:
        return right_set, left_set


def grow_set(the_set, track, ymin, ymax, xmin, xmax):
    remaining = deque(the_set)
    while remaining:
        current = remaining.popleft()
        for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            y, x = current[0] + dy, current[1] + dx
            if y < ymin or y > ymax or x < xmin or x > xmax:
                continue
            if (y, x) in the_set:
                continue
            if (y, x) in track:
                continue
            remaining.append((y, x))
            the_set.add((y, x))
    return the_set


def part2(inp):
    mz, start, ymin, ymax, xmin, xmax = parse(inp)
    track = find_track(mz, start)
    left1, right1 = find_left_and_right_set(mz, start, track, backward=False)
    left2, right2 = find_left_and_right_set(mz, start, track, backward=True)
    left, right = left1 | left2, right1 | right2
    left = grow_set(left, track, ymin, ymax, xmin, xmax)
    right = grow_set(right, track, ymin, ymax, xmin, xmax)
    if (0, 0) in left:
        return len(right)
    else:
        return len(left)


def test_1_1():
    assert 4 == part1(""".....
.S-7.
.|.|.
.L-J.
.....""")
    
def test_1_2():
    assert 8 == part1("""..F7.
.FJ|.
SJ.L7
|F--J
LJ...""")


def test_2_1():
    assert 4 == part2("""...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........""")


def test_2_2():
    assert 8 == part2(""".F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...""")


def test_2_3():
    assert 10 == part2("""FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L""")


def main(inp):
    print("Part1:", part1(inp.strip()))
    print("Part2:", part2(inp.strip()))


if __name__ == "__main__":
    prep = PrepareAoc(2023, 10)
    main(prep.get_content())