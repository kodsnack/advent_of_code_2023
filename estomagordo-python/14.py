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


def slide(grid, direction=(-1, 0)):
    h, w = dimensions(grid)
    dy, dx = direction

    if direction == (-1, 0):
        for y, x in product(range(h), range(w)):
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

        return grid

    if direction == (1, 0):
        for y in range(h-1, -1, -1):
            for x in range(w):
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

        return grid
    
    if direction == (0, -1):
        for y in range(h):
            for x in range(w):
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

        return grid
    
    for y in range(h):
        for x in range(w-1, -1, -1):
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
    grid = parse(lines)

    cycle_scores = defaultdict(list)
    cycle_scores[score(grid)].append(0)

    shifts = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    maxshifts = 2000

    for i in range(maxshifts):
        for shift in shifts:
            grid = slide(grid, shift)

        cycle_scores[score(grid)].append(i+1)

    totcycles = 1000000000

    for v in cycle_scores.values():
        if len(v) > 5:
            cyclen = v[4] - v[3]

            for k, v in cycle_scores.items():
                for i in v[4:]:
                    if (totcycles - i) % cyclen == 0:
                        return k


def main():
    lines = []

    with open('14.txt') as f:
        for line in f.readlines():
            lines.append(line.rstrip())
            
    return (solve_a(lines), solve_b(lines))


if __name__ == '__main__':
    print(main())
