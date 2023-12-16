from bisect import bisect, bisect_left, bisect_right
from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from math import ceil, comb, factorial, gcd, isclose, lcm

from algo import a_star, custsort, merge_ranges, sssp
from constants import EPSILON, HUGE
from helpers import adjacent, between, chunks, chunks_with_overlap, columns, digits, dimensions, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, overlap, positives, rays, rays_from_inside, words
   

def solve_a(lines):
    h, w = dimensions(lines)
    seen = set()
    done = set()

    frontier = [(0, 0, 1, 0)]

    for y, x, dy, dx in frontier:
        if (y, x, dy, dx) in done:
            continue

        done.add((y, x, dy, dx))
        seen.add((y, x))

        ny = y + dy
        nx = x + dx

        if not 0 <= ny < h:
            continue

        if not 0 <= nx < w:
            continue

        c = lines[ny][nx]

        if c == '.' or (c == '|' and dy != 0) or (c == '-' and dx != 0):
            if (ny, nx, dy, dx) in done:
                continue

            frontier.append((ny, nx, dy, dx))

        if c == '|':
            if (ny, nx, -1, 0) in done:
                continue
            frontier.append((ny, nx, -1, 0))

            if (ny, nx, 1, 0) in done:
                continue
            frontier.append((ny, nx, 1, 0))
        if c == '-':
            if (ny, nx, 0, -1) in done:
                continue
            frontier.append((ny, nx, 0, -1))

            if (ny, nx, 0, 1) in done:
                continue
            frontier.append((ny, nx, 0, 1))
        if c == '\\':
            ndy = -1 if dx == -1 else 1 if dx == 1 else 0
            ndx = -1 if dy == -1 else 1 if dy == 1 else 0

            if (ny, nx, ndy, ndx) in done:
                continue

            frontier.append((ny, nx, ndy, ndx))
        if c == '/':
            ndy = -1 if dx == 1 else 1 if dx == -1 else 0
            ndx = -1 if dy == 1 else 1 if dy == -1 else 0

            if (ny, nx, ndy, ndx) in done:
                continue

            frontier.append((ny, nx, ndy, ndx))

    for y in range(h):
        l = []

        for x in range(w):
            if (y, x) in seen:
                l.append('#')
            else:
                l.append('.')

        print(''.join(l))
    
    
    return len(seen)


def solve_b(lines):
    return 1


def main():
    lines = []

    with open('16.txt') as f:
        for line in f.readlines():
            lines.append(line.rstrip())
            
    return (solve_a(lines), solve_b(lines))


if __name__ == '__main__':
    print(main())
