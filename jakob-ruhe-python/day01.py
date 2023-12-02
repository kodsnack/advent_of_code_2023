#!/usr/bin/env python3

# By Jakob Ruhe 2023-12-01

import os


def parse_input(input):
    return input.strip().split("\n")


def digits():
    return {str(value): value for value in range(1, 10)}


def find_first_last(needle_map, haystack):
    first = None
    first_pos = len(haystack)
    last = None
    last_pos = -1
    for k, v in needle_map.items():
        p1 = haystack.find(k)
        if p1 >= 0 and p1 < first_pos:
            first = v
            first_pos = p1
        p2 = haystack.rfind(k)
        if p2 >= 0 and p2 > last_pos:
            last = v
            last_pos = p2
    return first, last


def num_from_line(needle_map, line):
    first, last = find_first_last(needle_map, line)
    return int(str(first) + str(last))


def solve(needle_map, entries):
    return sum([num_from_line(needle_map, line) for line in entries])


def solve1(entries):
    return solve(digits(), entries)


def digits_as_words():
    digits = ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine")
    return {v: k + 1 for k, v in enumerate(digits)}


def solve2(entries):
    return solve(digits() | digits_as_words(), entries)


if __name__ == "__main__":
    problem_name = os.path.splitext(os.path.basename(__file__))[0]
    with open(f"input/{problem_name}.txt") as f:
        entries = parse_input(f.read())
    print(solve1(entries))
    print(solve2(entries))
