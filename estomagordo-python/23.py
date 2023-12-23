from bisect import bisect_left, bisect_right
from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from math import ceil, comb, factorial, gcd, isclose, lcm

from algo import a_star, custsort, merge_ranges, sssp
from constants import EPSILON, HUGE
from helpers import adjacent, between, chunks, chunks_with_overlap, columns, digits, dimensions, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, overlap, positives, rays, rays_from_inside, words

from sys import setrecursionlimit

setrecursionlimit(10000)


def parse(lines):
    for x in range(len(lines[0])):
        if lines[0][x] == '.':
            return 0, x
        
    

def solve_a(lines):
    h, w = dimensions(lines)
    sy, sx = parse(lines)

    blockcount = sum(sum(c == '#' for c in row) for row in lines)

    print(sy, sx, h * w, blockcount)

    longest = [0]

    def walk(y, x, seen):
        if y == h-1:
            print(len(seen))
            longest[0] = max(longest[0], len(seen))
            return

        for ny, nx in neighs_bounded(y, x, 0, h-1, 0, w-1):
            if (ny, nx) in seen:
                continue

            c = lines[ny][nx]

            if c == '#':
                continue

            if c == '.':
                seen.add((ny, nx))
                walk(ny, nx, seen)
                seen.remove((ny, nx))
                continue

            dy = 1 if c == 'v' else -1 if c == '^' else 0
            dx = 1 if c == '>' else -1 if c == '<' else 0
            
            if (ny+dy, nx+dx) not in seen:
                seen.add((ny, nx))
                seen.add((ny+dy, nx+dx))
                walk(ny+dy, nx+dx, seen)
                seen.remove((ny, nx))
                seen.discard((ny+dy, nx+dx))


    walk(sy, sx, {(sy, sx)})

    return longest[0] - 1


def solve_b(lines):
    h, w = dimensions(lines)
    sy, sx = parse(lines)

    blockcount = sum(sum(c == '#' for c in row) for row in lines)

    print(sy, sx, h * w, blockcount)

    longest = [0]

    def walk(y, x, seen):
        if y == h-1:
            if len(seen) > longest[0]:
                print(len(seen))
                longest[0] = len(seen)
            return

        for ny, nx in neighs_bounded(y, x, 0, h-1, 0, w-1):
            if (ny, nx) in seen:
                continue

            c = lines[ny][nx]

            if c == '#':
                continue

            
            seen.add((ny, nx))
            walk(ny, nx, seen)
            seen.remove((ny, nx))
            continue

            dy = 1 if c == 'v' else -1 if c == '^' else 0
            dx = 1 if c == '>' else -1 if c == '<' else 0
            
            if (ny+dy, nx+dx) not in seen:
                seen.add((ny, nx))
                seen.add((ny+dy, nx+dx))
                walk(ny+dy, nx+dx, seen)
                seen.remove((ny, nx))
                seen.discard((ny+dy, nx+dx))


    walk(sy, sx, {(sy, sx)})

    return longest[0] - 1


def main():
    lines = []

    with open('23.txt') as f:
        for line in f.readlines():
            lines.append(line.rstrip())
            
    return (solve_a(lines), solve_b(lines))


if __name__ == '__main__':
    print(main())

# 6102