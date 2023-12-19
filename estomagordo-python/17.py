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

        for gy, gx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if gy * dy != 0 or gx * dx != 0:
                continue           
        
            cumsteps = 0

            for hops in range(1, maxsteps+1):
                py = y + hops * gy
                px = x + hops * gx

                if py < 0 or py >= h or px < 0 or px >= w:
                    break

                cumsteps += grid[y+hops*gy][x+hops*gx]

                if hops >= minsteps and (y + hops*gy, x + hops*gx, gy, gx) not in seen:
                    heappush(frontier, (steps + cumsteps, y + hops*gy, x + hops*gx, gy, gx))


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