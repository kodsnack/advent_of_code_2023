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
    frontier = [(grid[1][0], 1, 0, 1, 0), (grid[0][1], 0, 1, 0, 1)]

    while frontier:
        steps, y, x, dy, dx = heappop(frontier)

        if y == h-1 and x == w-1:
            return steps

        if (y, x, dy, dx) in seen:
            continue

        seen.add((y, x, dy, dx))
        
        canup = (dy > 0 or abs(dx) > minsteps-1) and dy >= 0 and dy < maxsteps and y < h-1 and (y+1, x, dy+1, 0) not in seen
        candown = (dy < 0 or abs(dx) > minsteps-1) and dy <= 0 and abs(dy) < maxsteps and y > 0 and (y-1, x, dy-1, 0) not in seen
        canright = (dx > 0 or abs(dy) > minsteps-1) and dx >= 0 and dx < maxsteps and x < w-1 and (y, x+1, 0, dx+1) not in seen
        canleft = (dx < 0 or abs(dy) > minsteps-1) and dx <= 0 and abs(dx) < maxsteps and x > 0 and (y, x-1, 0, dx-1) not in seen

        if canup:
            heappush(frontier, (steps + grid[y+1][x], y+1, x, dy+1, 0))
        if candown:
            heappush(frontier, (steps + grid[y-1][x], y-1, x, dy-1, 0))
        if canright:
            heappush(frontier, (steps + grid[y][x+1], y, x+1, 0, dx+1))
        if canleft:
            heappush(frontier, (steps + grid[y][x-1], y, x-1, 0, dx-1))

def solve_a(lines):
    return solve(lines, 0, 3)


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