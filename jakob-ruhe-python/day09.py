#!/usr/bin/env python3

# By Jakob Ruhe 2023-12-09

import os
import unittest


def parse_input(input):
    return input.strip().split("\n")


def solve(entries, getter):
    results = []
    for line in entries:
        numbers = [int(w) for w in line.split()]
        results.append(getter(numbers))
    return sum(results)


def get_next(numbers):
    if all(n == 0 for n in numbers):
        return 0
    next_gen = [numbers[i] - numbers[i - 1] for i in range(1, len(numbers))]
    return numbers[-1] + get_next(next_gen)


def solve1(entries):
    return solve(entries, get_next)


def get_prev(numbers):
    if all(n == 0 for n in numbers):
        return 0
    next_gen = [numbers[i] - numbers[i - 1] for i in range(1, len(numbers))]
    return numbers[0] - get_prev(next_gen)


def solve2(entries):
    return solve(entries, get_prev)


# Execute tests with:
# python3 -m unittest dayX
class TestThis(unittest.TestCase):
    input = """
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""

    def test1(self):
        self.assertEqual(solve1(parse_input(self.input)), 114)

    def test2(self):
        self.assertEqual(solve2(parse_input(self.input)), 2)


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    print(solve2(entries))
