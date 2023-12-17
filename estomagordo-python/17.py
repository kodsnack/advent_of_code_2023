from bisect import bisect, bisect_left, bisect_right
from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from math import ceil, comb, factorial, gcd, isclose, lcm

from algo import a_star, custsort, merge_ranges, sssp
from constants import EPSILON, HUGE
from helpers import adjacent, between, chunks, chunks_with_overlap, columns, digits, dimensions, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, overlap, positives, rays, rays_from_inside, words


def parse(lines):
    return [digits(line) for line in lines]


def solve_a(lines):
    grid = parse(lines)

    h, w = dimensions(grid)
    seen = {}
    frontier = [(0, 0, 0, 0, 0)]
    best = HUGE

    while frontier:
        steps, y, x, dy, dx = heappop(frontier)

        if y == h-1 and x == w-1:
            best = min(best, steps)
            continue

        if (y, x, dy, dx) in seen and seen[(y, x, dy, dx)] <= steps:
            continue

        seen[(y, x, dy, dx)] = steps

        if dy >= 0 and dy < 3 and y < h-1 and ((y+1, x, dy+1, 0) not in seen or seen[(y+1, x, dy+1, 0)] > steps + grid[y+1][x]):
            heappush(frontier, (steps + grid[y+1][x], y+1, x, dy+1, 0))
        if dy <= 0 and dy > -3 and y > 0 and ((y-1, x, dy-1, 0) not in seen or seen[(y-1, x, dy-1, 0)] > steps + grid[y-1][x]):
            heappush(frontier, (steps + grid[y-1][x], y-1, x, dy-1, 0))
        if dx >= 0 and dx < 3 and x < w-1 and ((y, x+1, 0, dx+1) not in seen or seen[(y, x+1, 0, dx+1)] > steps + grid[y][x+1]):
            heappush(frontier, (steps + grid[y][x+1], y, x+1, 0, dx+1))
        if dx <= 0 and dx > -3 and x > 0 and ((y, x-1, 0, dx-1) not in seen or seen[(y, x-1, 0, dx-1)] > steps + grid[y][x-1]):
            heappush(frontier, (steps + grid[y][x-1], y, x-1, 0, dx-1))

    return best


def solve_b(lines):
    grid = parse(lines)

    h, w = dimensions(grid)
    seen = {}
    frontier = [(grid[1][0], 1, 0, 1, 0), (grid[0][1], 0, 1, 0, 1)]
    best = HUGE

    while frontier:
        steps, y, x, dy, dx = heappop(frontier)

        if y == h-1 and x == w-1:
            best = min(best, steps)
            continue

        if (y, x, dy, dx) in seen and seen[(y, x, dy, dx)] <= steps:
            continue

        seen[(y, x, dy, dx)] = steps        

        if (dy > 0 or abs(dx) > 3) and dy >= 0 and dy < 10 and y < h-1 and ((y+1, x, dy+1, 0) not in seen or seen[(y+1, x, dy+1, 0)] > steps + grid[y+1][x]):
            heappush(frontier, (steps + grid[y+1][x], y+1, x, dy+1, 0))
        if (dy < 0 or abs(dx) > 3) and dy <= 0 and dy > -10 and y > 0 and ((y-1, x, dy-1, 0) not in seen or seen[(y-1, x, dy-1, 0)] > steps + grid[y-1][x]):
            heappush(frontier, (steps + grid[y-1][x], y-1, x, dy-1, 0))
        if (dx > 0 or abs(dy) > 3) and dx >= 0 and dx < 10 and x < w-1 and ((y, x+1, 0, dx+1) not in seen or seen[(y, x+1, 0, dx+1)] > steps + grid[y][x+1]):
            heappush(frontier, (steps + grid[y][x+1], y, x+1, 0, dx+1))
        if (dx < 0 or abs(dy) > 3) and dx <= 0 and dx > -10 and x > 0 and ((y, x-1, 0, dx-1) not in seen or seen[(y, x-1, 0, dx-1)] > steps + grid[y][x-1]):
            heappush(frontier, (steps + grid[y][x-1], y, x-1, 0, dx-1))

    return best


def main():
    lines = []

    with open('17.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return (solve_a(lines), solve_b(lines))


if __name__ == '__main__':
    print(main())