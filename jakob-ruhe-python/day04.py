#!/usr/bin/env python3

# By Jakob Ruhe 2023-12-04

import os
import unittest
from collections import defaultdict


def parse_input(input):
    return input.strip().split("\n")


def parse_line(line):
    _, all_cards = line.split(":")
    winning, cards = all_cards.split("|")
    return tuple(int(w) for w in winning.split()), tuple(int(w) for w in cards.split())


def num_matching(winning, cards):
    return len(list(filter(lambda c: c in winning, cards)))


def solve1(entries):
    total = 0
    for line in entries:
        winning, cards = parse_line(line)
        if (num_won := num_matching(winning, cards)) > 0:
            points = 2 ** (num_won - 1)
            total += points
    return total


def solve2(entries):
    num_cards = defaultdict(int)
    for i, line in enumerate(entries):
        num_cards[i] += 1
        winning, cards = parse_line(line)
        num_won = num_matching(winning, cards)
        for j in range(num_won):
            num_cards[j + i + 1] += num_cards[i]
    return sum(num_cards.values())


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""

    def test1(self):
        self.assertEqual(solve1(parse_input(self.input)), 13)

    def test2(self):
        self.assertEqual(solve2(parse_input(self.input)), 30)


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    print(solve2(entries))
