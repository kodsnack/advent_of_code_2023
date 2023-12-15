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
    return [list(line) for line in lines]


def slide(grid, direction=(-1, 0)):
    h, w = dimensions(grid)
    dy, dx = direction
    ycoords = range(h) if dy <= 0 else range(h-1, -1, -1)
    xcoords = range(w) if dx <= 0 else range(w-1, -1, -1)
    
    for y, x in product(ycoords, xcoords):
        c = grid[y][x]

        if c != 'O':
            continue

        my = y
        mx = x

        while 0 <= my+dy < h and 0 <= mx+dx < w and grid[my+dy][mx+dx] == '.':
            grid[my+dy][mx+dx] = 'O'
            grid[my][mx] = '.'

            my += dy
            mx += dx


def score(grid):
    h, w = dimensions(grid)

    return sum(0 if grid[y][x] != 'O' else h-y + HUGE * x for y, x in product(range(h), range(w)))


def solve_a(lines):
    grid = parse(lines)

    slide(grid)

    return score(grid) % HUGE


def solve_b(lines):
    grid = parse(lines)

    cycle_scores = defaultdict(list)
    cycle_scores[score(grid)].append(0)

    shifts = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    totcycles = 1000000000
    
    i = 1

    while True:
        for shift in shifts:
            slide(grid, shift)

        s = score(grid)
        
        cycle_scores[s].append(i)

        if len(cycle_scores[s]) > 1:
            diff = i - cycle_scores[s][-2]

            if (totcycles - i) % diff == 0:
                return s % HUGE

        i += 1


def main():
    lines = []

    with open('14.txt') as f:
        for line in f.readlines():
            lines.append(line.rstrip())
            
    return (solve_a(lines), solve_b(lines))


if __name__ == '__main__':
    print(main())
