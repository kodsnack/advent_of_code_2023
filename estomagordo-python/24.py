from bisect import bisect_left, bisect_right
from collections import Counter, defaultdict, deque
from fractions import Fraction
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from math import ceil, comb, factorial, gcd, isclose, lcm

from algo import a_star, custsort, merge_ranges, sssp
from constants import EPSILON, HUGE, UNHUGE
from helpers import adjacent, between, chunks, chunks_with_overlap, columns, digits, dimensions, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, overlap, positives, rays, rays_from_inside, solve_system, words


def parse(lines):
    intlines = [ints(line) for line in lines]

    return [[Fraction(num) for num in line] for line in intlines]
    

def kmform(line):
    k = line[4] / line[3]
    t = -line[0] / line[3]
    m = line[1] + t * line[4]

    return k, m


def intersect(a, b, minval, maxval):
    ak, am = kmform(a)
    bk, bm = kmform(b)

    if ak == bk:
        return False

    x = (bm - am) / (ak - bk)

    if x < minval or x > maxval:
        return False
    
    ta = (x - a[0]) / a[3]
    tb = (x - b[0]) / b[3]

    if ta < 0:
        return False
    
    if tb < 0:
        return False
    
    y = a[1] + a[4] * ta

    return minval <= y <= maxval


def solve_a(lines):
    minval = 200000000000000
    maxval = 400000000000000

    hailstones = parse(lines)

    return sum(intersect(a, b, minval, maxval) for a, b in combinations(hailstones, 2))


def collides_in_future(stone, rock):
    sx, sy, sz, dsx, dsy, dsz = stone
    rx, ry, rz, drx, dry, drz = rock

    stricttx = True
    strictty = True
    stricttz = True
    
    match_x_const = sx - rx
    match_x_vari = drx - dsx

    if match_x_vari == 0:
        if match_x_const != 0:
            return False
        stricttx = False

    tx = Fraction(1) if not stricttx else match_x_const / match_x_vari

    if stricttx and tx < 0:
        return False
    
    match_y_const = sy - ry
    match_y_vari = dry - dsy

    if match_y_vari == 0:
        if match_y_const != 0:
            return False
        strictty = False

    ty = Fraction(1) if not strictty else match_y_const / match_y_vari

    if stricttx and strictty and ty != tx:
        return False
    
    if strictty and ty < 0:
        return False
    
    match_z_const = sz - rz
    match_z_vari = drz - dsz

    if match_z_vari == 0:
        if match_z_const != 0:
            return False
        stricttz = False

    tz = Fraction(1) if not stricttz else match_z_const / match_z_vari

    if stricttz and tz < 0:
        return False

    if stricttx and strictty and stricttz:
        return tx == ty == tz

    if not stricttz:
        return True
    
    if stricttx:
        return tz == tx
    
    if strictty:
        return tz == ty
    
    return True


def is_solution(hailstones, rock):
    return all(collides_in_future(stone, rock) for stone in hailstones)


def find_solution(dx, dy, x1, x2, y1, y2, dx1, dx2, dy1, dy2):
    equations = [
        [1, 0, dx - dx1, 0, x1],
        [1, 0, 0, dx - dx2, x2],
        [0, 1, dy - dy1, 0, y1],
        [0, 1, 0, dy - dy2, y2]
    ]

    equations = [[Fraction(val) for val in row] for row in equations]

    solves, reduced = solve_system(equations)

    return solves, *reduced


def solve_b(lines):
    hailstones = parse(lines)

    x1 = hailstones[0][0]
    x2 = hailstones[1][0]
    y1 = hailstones[0][1]
    y2 = hailstones[1][1]
    dx1 = hailstones[0][3]
    dx2 = hailstones[1][3]
    dy1 = hailstones[0][4]
    dy2 = hailstones[1][4]

    span = 500

    for dx in range(-span, span):
        for dy in range(-span, span):
            solves, x, y, t1, t2 = find_solution(Fraction(dx), Fraction(dy), x1, x2, y1, y2, dx1, dx2, dy1, dy2)

            if not solves:
                continue

            if t1 < 0 or t2 < 0:
                continue

            z1 = hailstones[0][2] + hailstones[0][5] * t1
            z2 = hailstones[1][2] + hailstones[1][5] * t2

            z = dz = Fraction(0)

            if t1 == t2:
                continue

            if t2 > t1:
                dz = (z2 - z1) / (t2 - t1)
                z = z1 - dz * t1
            else:
                dz = (z1 - z2) / (t1 - t2)
                
                if dz != int(dz):
                    continue

                dz = int(dz)

                z = z2 - dz * t2

            stone = [Fraction(num) for num in (x, y, z, dx, dy, dz)]

            if is_solution(hailstones, stone):
                return int(x + y + z)


def main():
    lines = []

    with open('24.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return (solve_a(lines), solve_b(lines))


if __name__ == '__main__':
    print(main())