from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from math import ceil, comb, factorial, gcd, isclose, lcm

from algo import a_star, custsort, merge_ranges, sssp
from constants import EPSILON
from helpers import adjacent, between, chunks, chunks_with_overlap, columns, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, overlap, positives, rays, rays_from_inside, words


def solve(lines, spacing):
    empty = {'.'}

    galaxies = set()
    empty_cols = []
    empty_rows = []

    for y in range(len(lines)):
        if set(lines[y]) == empty:
            empty_rows.append(y)

        for x in range(len(lines[0])):
            if lines[y][x] == '#':
                galaxies.add((y, x))

    for x, col in enumerate(columns(lines)):
        if set(col) == empty:
            empty_cols.append(x)

    def distance(a, b):
        expanded_rows = sum(between(row, a[0], b[0]) for row in empty_rows)
        expanded_cols = sum(between(col, a[1], b[1]) for col in empty_cols)
        base_distance = manhattan(a, b)

        return base_distance + (expanded_rows + expanded_cols) * spacing
    
    return sum(distance(a, b) for a, b in combinations(galaxies, 2))
    

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