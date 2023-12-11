from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from math import ceil, comb, factorial, gcd, isclose, lcm

from algo import a_star, custsort, merge_ranges, sssp
from constants import EPSILON
from helpers import adjacent, chunks, chunks_with_overlap, columns, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, overlap, positives, rays, rays_from_inside, words


def solve(lines, spacing):
    galaxies = set()
    empty_cols = set()
    empty_rows = set()

    for y in range(len(lines)):
        if set(lines[y]) == {'.'}:
            empty_rows.add(y)

        for x in range(len(lines[0])):
            if lines[y][x] == '#':
                galaxies.add((y, x))

    for x, col in enumerate(columns(lines)):
        if set(col) == {'.'}:
            empty_cols.add(x)

    total = 0

    for gy, gx in galaxies:
        found = {(gy, gx)}
        seen = set()
        frontier = [(0, gy, gx)]

        while len(found) < len(galaxies):
            steps, y, x = heappop(frontier)

            if (y, x) in seen:
                continue

            if (y, x) in galaxies:
                found.add((y, x))
                total += steps

            seen.add((y, x))

            for ny, nx in neighs_bounded(y, x, 0, len(lines)-1, 0, len(lines[0])-1):
                if (ny, nx) in seen:
                    continue

                cost = 1 + spacing * (ny in empty_rows) + spacing * (nx in empty_cols)

                heappush(frontier, (steps+cost, ny, nx))

    return total // 2
    

def solve_a(lines):
    return solve(lines, 1)


def solve_b(lines):
    return solve(lines, 999999)


def main():
    lines = []

    with open('11.txt') as f:
        for line in f.readlines():
            lines.append(line.rstrip())
            
    return (solve_a(lines), solve_b(lines))


if __name__ == '__main__':
    print(main())