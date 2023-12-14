#!/usr/bin/env python3

# By Jakob Ruhe 2023-12-11

import os
import unittest
from collections import namedtuple
import itertools


Point = namedtuple("Point", ["x", "y"])


def parse_input(input):
    return input.strip().split("\n")


def expand_rows(grid, add):
    grid_out = set()
    rows = {}
    for p in grid:
        if not p.y in rows:
            rows[p.y] = []
        rows[p.y].append(p)
    h = max([p.y for p in grid]) + 1
    dy = 0
    for y in range(h):
        if y in rows:
            for p in rows[y]:
                grid_out.add(Point(p.x, dy))
            dy += 1
        else:
            dy += add
    return grid_out


def expand_cols(grid, add):
    grid_out = set()
    cols = {}
    for p in grid:
        if not p.x in cols:
            cols[p.x] = []
        cols[p.x].append(p)
    w = max([p.x for p in grid]) + 1
    dx = 0
    for x in range(w):
        if x in cols:
            for p in cols[x]:
                grid_out.add(Point(dx, p.y))
            dx += 1
        else:
            dx += add
    return grid_out


def build_grid(entries):
    grid = set()
    for y, line in enumerate(entries):
        for x, c in enumerate(line):
            if c == "#":
                grid.add(Point(x, y))
    return grid


def solve(entries, expand):
    grid = build_grid(entries)
    stars = list(expand_cols(expand_rows(grid, expand), expand))
    combinations = set(itertools.combinations(range(len(stars)), 2))
    distances = []
    for c in combinations:
        p1 = stars[c[0]]
        p2 = stars[c[1]]
        dist = abs(p1.x - p2.x) + abs(p1.y - p2.y)
        distances.append(dist)
    return sum(distances)


def solve1(entries):
    return solve(entries, 2)


def solve2(entries):
    return solve(entries, 1000000)


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""

    def test1(self):
        self.assertEqual(solve1(parse_input(self.input)), 374)

    def test2(self):
        self.assertEqual(solve(parse_input(self.input), 10), 1030)
        self.assertEqual(solve(parse_input(self.input), 100), 8410)


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    print(solve2(entries))
