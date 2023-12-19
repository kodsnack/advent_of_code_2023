from bisect import bisect_left, bisect_right
from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from math import ceil, comb, factorial, gcd, isclose, lcm

from algo import a_star, custsort, merge_ranges, sssp
from constants import EPSILON, HUGE
from helpers import adjacent, between, chunks, chunks_with_overlap, columns, digits, dimensions, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, overlap, positives, rays, rays_from_inside, rim, words


def solve(lines, sy, sx, sdy, sdx):
    h, w = dimensions(lines)

    seen = set()
    done = set()

    frontier = [(sy, sx, sdy, sdx)]

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
        skipping = False

        while c == '.' or (c == '|' and dy != 0) or (c == '-' and dx != 0):
            done.add((ny, nx, dy, dx))
            seen.add((ny, nx))

            ny += dy
            nx += dx

            if ny in (-1, h) or nx in (-1, w):
                skipping = True
                break

            c = lines[ny][nx]

        if skipping:
            continue

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
            ndy = dx
            ndx = dy

            if (ny, nx, ndy, ndx) in done:
                continue

            frontier.append((ny, nx, ndy, ndx))
        if c == '/':
            ndy = -dx
            ndx = -dy

            if (ny, nx, ndy, ndx) in done:
                continue

            frontier.append((ny, nx, ndy, ndx))

    return len(seen)


def solve_a(lines):
    dy = 1 if lines[0][0] in '\\|' else 0
    dx = 1 - dy

    return solve(lines, 0, 0, dy, dx)


def solve_b(lines):
    h, w = dimensions(lines)
    starts = []

    for y in range(h):        
        left = lines[y][0]

        if left == '\\':
            starts.append((y, 0, 1, 0))
        elif left == '/':
            starts.append((y, 0, -1, 0))
        else:
            starts.append((y, 0, 0, 1))

        right = lines[y][w-1]

        if right == '\\':
            starts.append((y, w-1, -1, 0))
        elif right == '/':
            starts.append((y, w-1, 1, 0))
        else:
            starts.append((y, w-1, 0, -1))

    for x in range(w):
        down = lines[0][x]

        if down == '\\':
            starts.append((0, x, 0, 1))
        elif down == '/':
            starts.append((0, x, 0, -1))
        else:
            starts.append((0, x, 1, 0))

        up = lines[y][w-1]

        if up == '\\':
            starts.append((h-1, x, 0, -1))
        elif up == '/':
            starts.append((h-1, x, 0, 1))
        else:
            starts.append((h-1, x, -1, 0))

    return max(solve(lines, sy, sx, sdy, sdx) for sy, sx, sdy, sdx in starts)


def main():
    lines = []

    with open('16.txt') as f:
        for line in f.readlines():
            lines.append(line.rstrip())
            
    return (solve_a(lines), solve_b(lines))


if __name__ == '__main__':
    print(main())
