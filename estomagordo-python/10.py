from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from math import ceil, comb, factorial, gcd, isclose, lcm

from algo import a_star, custsort, merge_ranges, sssp
from constants import EPSILON
from helpers import adjacent, chunks, chunks_with_overlap, columns, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, overlap, positives, rays, rays_from_inside, words


def parse(lines):
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            if lines[y][x] == 'S':
                return y, x
    

def solve_a(lines):
    sy, sx = parse(lines)
    h = len(lines)
    w = len(lines[0])

    seen = {(sy, sx): 0}
    frontier = []

    if sy > 0 and lines[sy-1][sx] in '|7F':
        frontier.append((1, sy-1, sx))        
    if sy < h-1 and lines[sy+1][sx] in '|LJ':
        frontier.append((1, sy+1, sx))
    if sx > 0 and lines[sy][sx-1] in '-LF':
        frontier.append((1, sy, sx+1))        
    if sx < w-1 and lines[sy][sx+1] in '-J7':
        frontier.append((1, sy, sx+1))

    for steps, y, x in frontier:
        if (y, x) in seen:
            continue

        seen[(y, x)] = steps

        c = lines[y][x]
        cangoup = y > 0
        cangodown = y < h - 1
        cangoleft = x > 0
        cangoright = x < w - 1

        match c:
            case '|':
                if cangodown and (y+1, x) not in seen:
                    frontier.append((steps+1, y+1, x))
                if cangoup and (y-1, x) not in seen:
                    frontier.append((steps+1, y-1, x))
            case '-':
                if cangoleft and (y, x-1) not in seen:
                    frontier.append((steps+1, y, x-1))
                if cangoright and (y, x+1) not in seen:
                    frontier.append((steps+1, y, x+1))
            case 'L':
                if cangoup and (y-1, x) not in seen:
                    frontier.append((steps+1, y-1, x))
                if cangoright and (y, x+1) not in seen:
                    frontier.append((steps+1, y, x+1))
            case 'J':
                if cangoleft and (y, x-1) not in seen:
                    frontier.append((steps+1, y, x-1))
                if cangoup and (y-1, x) not in seen:
                    frontier.append((steps+1, y-1, x))
            case '7':
                if cangoleft and (y, x-1) not in seen:
                    frontier.append((steps+1, y, x-1))
                if cangodown and (y+1, x) not in seen:
                    frontier.append((steps+1, y+1, x))
            case 'F':
                if cangodown and (y+1, x) not in seen:
                    frontier.append((steps+1, y+1, x))
                if cangoright and (y, x+1) not in seen:
                    frontier.append((steps+1, y, x+1))

    return max(seen.values())


def solve_b(lines):
    sy, sx = parse(lines)
    h = len(lines)
    w = len(lines[0])

    seen = {(sy, sx): 0}
    frontier = []

    if sy > 0 and lines[sy-1][sx] in '|7F':
        frontier.append((1, sy-1, sx))        
    if sy < h-1 and lines[sy+1][sx] in '|LJ':
        frontier.append((1, sy+1, sx))
    if sx > 0 and lines[sy][sx-1] in '-LF':
        frontier.append((1, sy, sx+1))        
    if sx < w-1 and lines[sy][sx+1] in '-J7':
        frontier.append((1, sy, sx+1))

    for steps, y, x in frontier:
        if (y, x) in seen:
            continue

        seen[(y, x)] = steps

        c = lines[y][x]
        cangoup = y > 0
        cangodown = y < h - 1
        cangoleft = x > 0
        cangoright = x < w - 1

        match c:
            case '|':
                if cangodown and (y+1, x) not in seen:
                    frontier.append((steps+1, y+1, x))
                if cangoup and (y-1, x) not in seen:
                    frontier.append((steps+1, y-1, x))
            case '-':
                if cangoleft and (y, x-1) not in seen:
                    frontier.append((steps+1, y, x-1))
                if cangoright and (y, x+1) not in seen:
                    frontier.append((steps+1, y, x+1))
            case 'L':
                if cangoup and (y-1, x) not in seen:
                    frontier.append((steps+1, y-1, x))
                if cangoright and (y, x+1) not in seen:
                    frontier.append((steps+1, y, x+1))
            case 'J':
                if cangoleft and (y, x-1) not in seen:
                    frontier.append((steps+1, y, x-1))
                if cangoup and (y-1, x) not in seen:
                    frontier.append((steps+1, y-1, x))
            case '7':
                if cangoleft and (y, x-1) not in seen:
                    frontier.append((steps+1, y, x-1))
                if cangodown and (y+1, x) not in seen:
                    frontier.append((steps+1, y+1, x))
            case 'F':
                if cangodown and (y+1, x) not in seen:
                    frontier.append((steps+1, y+1, x))
                if cangoright and (y, x+1) not in seen:
                    frontier.append((steps+1, y, x+1))

    frontier = []

    for y in range(h):
        if lines[y][0] == '.':
            frontier.append((y, 0))
        if lines[y][w-1] == '.':
            frontier.append((y, w-1))

    for x in range(w):
        if lines[0][x] == '.':
            frontier.append((0, x))
        if lines[h-1][x] == '.':
            frontier.append((h-1, x))

    outside = set()

    for y, x in frontier:
        if (y, x) in outside:
            continue

        outside.add((y, x))

        for ny, nx in neighs_bounded(y, x, 0, h-1, 0, w-1):
            if (ny, nx) in outside or (ny, nx) in seen:
                continue

            frontier.append((ny, nx))

    return h*w - len(seen) - len(outside)


def main():
    lines = []

    with open('10.txt') as f:
        for line in f.readlines():
            lines.append(line.rstrip())
            
    return (solve_a(lines), solve_b(lines))


if __name__ == '__main__':
    print(main())