from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from math import ceil, comb, factorial, gcd, isclose, lcm

from algo import a_star, custsort, merge_ranges, sssp
from constants import EPSILON
from helpers import adjacent, chunks, chunks_with_overlap, columns, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, overlap, positives, rays, rays_from_inside, words


def find_path(lines):
    sy = -1
    sx = -1

    for y in range(len(lines)):
        for x in range(len(lines[0])):
            if lines[y][x] == 'S':
                sy = y
                sx = x

    h = len(lines)
    w = len(lines[0])

    path = {(sy, sx): 0}
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
        if (y, x) in path:
            continue

        path[(y, x)] = steps

        c = lines[y][x]
        cangoup = y > 0
        cangodown = y < h - 1
        cangoleft = x > 0
        cangoright = x < w - 1

        match c:
            case '|':
                if cangodown and (y+1, x) not in path:
                    frontier.append((steps+1, y+1, x))
                if cangoup and (y-1, x) not in path:
                    frontier.append((steps+1, y-1, x))
            case '-':
                if cangoleft and (y, x-1) not in path:
                    frontier.append((steps+1, y, x-1))
                if cangoright and (y, x+1) not in path:
                    frontier.append((steps+1, y, x+1))
            case 'L':
                if cangoup and (y-1, x) not in path:
                    frontier.append((steps+1, y-1, x))
                if cangoright and (y, x+1) not in path:
                    frontier.append((steps+1, y, x+1))
            case 'J':
                if cangoleft and (y, x-1) not in path:
                    frontier.append((steps+1, y, x-1))
                if cangoup and (y-1, x) not in path:
                    frontier.append((steps+1, y-1, x))
            case '7':
                if cangoleft and (y, x-1) not in path:
                    frontier.append((steps+1, y, x-1))
                if cangodown and (y+1, x) not in path:
                    frontier.append((steps+1, y+1, x))
            case 'F':
                if cangodown and (y+1, x) not in path:
                    frontier.append((steps+1, y+1, x))
                if cangoright and (y, x+1) not in path:
                    frontier.append((steps+1, y, x+1))

    return path
    

def solve_a(lines):
    path = find_path(lines)

    return max(path.values())


def is_inside(lines, path, y, x):
    if (y, x) in path:
        return False    
    
    return sum(lines[y][lx] in 'LJ|' and (y, lx) in path for lx in range(x)) % 2


def solve_b(lines):    
    path = find_path(lines)

    return sum(is_inside(lines, path, y, x) for y in range(len(lines)) for x in range(len(lines[0])))


def main():
    lines = []

    with open('10.txt') as f:
        for line in f.readlines():
            lines.append(line.rstrip())
            
    return (solve_a(lines), solve_b(lines))


if __name__ == '__main__':
    print(main())