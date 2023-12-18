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


def solve(lines, minsteps, maxsteps):
    grid = parse(lines)
    h, w = dimensions(grid)
    
    seen = set()
    frontier = [(0, 0, 0, 0, 0)]

    while frontier:
        steps, y, x, dy, dx = heappop(frontier)

        if y == h-1 and x == w-1:
            return steps

        if (y, x, dy, dx) in seen:
            continue

        seen.add((y, x, dy, dx))

        if dy == 0:
            cumsteps = 0

            for hops in range(1, maxsteps+1):
                if y + hops >= h:
                    break

                cumsteps += grid[y+hops][x]

                if hops >= minsteps and (y + hops, x, 1, 0) not in seen:
                    heappush(frontier, (steps + cumsteps, y + hops, x, 1, 0))

        if dy == 0:
            cumsteps = 0

            for hops in range(1, maxsteps+1):
                if y - hops < 0:
                    break

                cumsteps += grid[y-hops][x]

                if hops >= minsteps and (y - hops, x, -1, 0) not in seen:
                    heappush(frontier, (steps + cumsteps, y - hops, x, -1, 0))

        if dx == 0:
            cumsteps = 0

            for hops in range(1, maxsteps+1):
                if x + hops >= w:
                    break

                cumsteps += grid[y][x+hops]

                if hops >= minsteps and (y, x + hops, 0, 1) not in seen:
                    heappush(frontier, (steps + cumsteps, y, x + hops, 0, 1))

        if dx == 0:
            cumsteps = 0

            for hops in range(1, maxsteps+1):
                if x - hops < 0:
                    break

                cumsteps += grid[y][x-hops]

                if hops >= minsteps and (y, x - hops, 0, -1) not in seen:
                    heappush(frontier, (steps + cumsteps, y, x - hops, 0, -1))


def solve_a(lines):
    return solve(lines, 1, 3)


def solve_b(lines):
    return solve(lines, 4, 10)


def main():
    lines = []

    with open('17.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return (solve_a(lines), solve_b(lines))


if __name__ == '__main__':
    print(main())