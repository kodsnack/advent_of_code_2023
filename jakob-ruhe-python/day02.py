#!/usr/bin/env python3

# By Jakob Ruhe 2023-12-02

import os
import math
import unittest
from collections import defaultdict


def parse_input(input):
    return input.strip().split("\n")


def parse_line(line):
    _, subsets_str = line.split(":")
    subsets = []
    for subset in subsets_str.strip().split(";"):
        shows = defaultdict(int)
        for show in subset.split(","):
            num, color = show.strip().split()
            shows[color] += int(num)
        subsets.append(shows)
    return subsets


def is_possible_game(max_possible, subsets):
    for subset in subsets:
        for k, v in max_possible.items():
            if subset.get(k, 0) > v:
                return False
    return True


def solve1(lines):
    max_possible = {"red": 12, "green": 13, "blue": 14}
    possible = [
        i + 1
        for i, line in enumerate(lines)
        if is_possible_game(max_possible, parse_line(line))
    ]
    return sum(possible)


def power_of_game(subsets):
    colors = ("red", "green", "blue")
    subset_min = defaultdict(int)
    for subset in subsets:
        for color in colors:
            subset_min[color] = max(subset_min[color], subset.get(color, 0))
    return math.prod(subset_min.values())


def solve2(lines):
    return sum([power_of_game(parse_line(line)) for line in lines])


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""

    def test1(self):
        self.assertEqual(solve1(parse_input(self.input)), 8)

    def test2(self):
        self.assertEqual(solve2(parse_input(self.input)), 2286)


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    print(solve2(entries))
