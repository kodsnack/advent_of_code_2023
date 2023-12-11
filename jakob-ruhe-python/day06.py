#!/usr/bin/env python3

# By Jakob Ruhe 2023-12-06

import os
import unittest
import math


def parse_input(input):
    return input.strip().split("\n")


def num_winning_ways(total_time, min_dist):
    # Equation to solve:
    # t * (total_time - t) > min_dist
    half_time = total_time / 2
    A = math.sqrt(math.pow(half_time, 2) - min_dist)
    t1 = half_time - A
    t2 = half_time + A
    eps = 1e-6
    tt1 = math.ceil(t1 + eps)
    tt2 = math.floor(t2 - eps)
    return int(tt2 - tt1) + 1


def solve1(entries):
    times = tuple(int(w) for w in entries[0].split(":")[1].split())
    distances = tuple(int(w) for w in entries[1].split(":")[1].split())
    num_ways = []
    for t, d in zip(times, distances):
        num_ways.append(num_winning_ways(t, d))
    return math.prod(num_ways)


def solve2(entries):
    total_time = int("".join(filter(str.isdigit, entries[0])))
    min_dist = int("".join(filter(str.isdigit, entries[1])))
    return num_winning_ways(total_time, min_dist)


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
Time:      7  15   30
Distance:  9  40  200
"""

    def test1(self):
        self.assertEqual(solve1(parse_input(self.input)), 288)

    def test2(self):
        self.assertEqual(solve2(parse_input(self.input)), 71503)


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    print(solve2(entries))
