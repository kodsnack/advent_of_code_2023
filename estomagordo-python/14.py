from bisect import bisect, bisect_left, bisect_right
from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from math import ceil, comb, factorial, gcd, isclose, lcm

from algo import a_star, custsort, merge_ranges, sssp
from constants import EPSILON
from helpers import adjacent, between, chunks, chunks_with_overlap, columns, digits, dimensions, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, overlap, positives, rays, rays_from_inside, words
    

def parse(lines):
    return [list(line) for line in lines]


def slide(grid):
    h, w = dimensions(grid)    

    for y, x in product(range(h), range(w)):
        if y == 0:
            continue

        c = grid[y][x]

        if c != 'O':
            continue

        dy = y
        my = dy-1

        while my >= 0 and grid[my][x] == '.':
            grid[my][x] = 'O'
            grid[dy][x] = '.'

            dy -= 1
            my -= 1

    return grid


def score(grid):
    h, w = dimensions(grid)
    s = 0

    for y, x in product(range(h), range(w)):
        if grid[y][x] == 'O':
            s += h-y

    return s


def solve_a(lines):
    grid = parse(lines)

    grid = slide(grid)

    return score(grid)


def solve_b(lines):
    data = parse(lines)

    return None


def main():
    lines = []

    with open('14.txt') as f:
        for line in f.readlines():
            lines.append(line.rstrip())
            
    return (solve_a(lines), solve_b(lines))


if __name__ == '__main__':
    print(main())
