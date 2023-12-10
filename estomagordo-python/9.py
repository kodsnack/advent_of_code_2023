from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from math import ceil, comb, factorial, gcd, isclose, lcm

from algo import a_star, custsort, merge_ranges, sssp
from constants import EPSILON
from helpers import adjacent, chunks, chunks_with_overlap, columns, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, overlap, positives, rays, rays_from_inside, words


def parse(lines):
    return [ints(line) for line in lines]


def solve_line(line):
    rows = [line]

    while any(v != 0 for v in rows[-1]):
        latest = rows[-1]
        newdiffs = []

        for i in range(1, len(latest)):
            newdiffs.append(latest[i] - latest[i-1])

        rows.append(newdiffs)

    rows[-1].append(0)

    for j in range(len(rows) - 2, -1, -1):
        rows[j].append(rows[j+1][-1] + rows[j][-1])

    return rows[0][-1]


def solve_line_b(line):
    rows = [line]

    while any(v != 0 for v in rows[-1]):
        latest = rows[-1]
        newdiffs = []

        for i in range(1, len(latest)):
            newdiffs.append(latest[i] - latest[i-1])

        rows.append(newdiffs)

    rows[-1].append(0)

    for j in range(len(rows) - 2, -1, -1):
        rows[j] = [rows[j][0] - rows[j+1][0]] + rows[j]

    return rows[0][0]
    

def solve_a(lines):
    data = parse(lines)

    return sum(solve_line(d) for d in data)


def solve_b(lines):
    data = parse(lines)

    return sum(solve_line_b(d) for d in data)


def main():
    lines = []

    with open('9.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return (solve_a(lines), solve_b(lines))


if __name__ == '__main__':
    print(main())