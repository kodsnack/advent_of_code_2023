from bisect import bisect_left, bisect_right
from collections import Counter, defaultdict, deque
from fractions import Fraction
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from math import ceil, comb, factorial, gcd, isclose, lcm

from algo import a_star, custsort, merge_ranges, sssp
from constants import EPSILON, HUGE, UNHUGE
from helpers import adjacent, between, chunks, chunks_with_overlap, columns, digits, dimensions, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, overlap, positives, rays, rays_from_inside, words


def parse(lines):
    return [ints(line) for line in lines]
    

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


def dimension_can_be_reached(stone, rock, dimension):
    s, ds, r, dr = stone[dimension], stone[dimension+3], rock[dimension], rock[dimension + 3]

    if ds > 0:
        if dr > 0:
            if ds > dr:
                if s > r:
                    return False
            elif r > s:
                return False
        elif s > r:
            return False
    else:
        if dr < 0:
            if ds < dr:
                if s < r:
                    return False
            elif r < s:
                return False
        elif s < r:
            return False

    return True


def stone_can_be_reached(stone, rock):
    return all(dimension_can_be_reached(stone, rock, dimension) for dimension in range(3))


def collidesall(hailstones, rock):
    if not all(stone_can_be_reached(stone, rock) for stone in hailstones):
        return False
    
    collided = set()
    maxsteps = 5000
    breaker = 25
    lastcollided = -1

    for t in range(1, maxsteps):
        if len(collided) == len(hailstones):
            return True
        
        if t - lastcollided > breaker:
            break
        
        rx = rock[0] + rock[3] * t
        ry = rock[1] + rock[4] * t
        rz = rock[2] + rock[5] * t

        for i, hailstone in enumerate(hailstones):
            sx = Fraction(hailstone[0]) + Fraction(hailstone[3]) * t
            sy = Fraction(hailstone[1]) + Fraction(hailstone[4]) * t
            sz = Fraction(hailstone[2]) + Fraction(hailstone[5]) * t

            if rx == sx and ry == sy and rz == sz:
                collided.add(i)
                lastcollided = t

    # print('attempt', len(collided), lastcollided, maxsteps)
    return False


def solve_b(lines):
    hailstones = parse(lines)

    maxxifplusx = HUGE
    minxifnegx = UNHUGE
    maxyifplusy = HUGE
    minyifnegy = UNHUGE
    maxzifplusz = HUGE
    minzifnegz = UNHUGE

    for x, y, z, dx, dy, dz in hailstones:
        if dx > 0:
            minxifnegx = max(minxifnegx, x)
        else:
            maxxifplusx = min(maxxifplusx, x)
        if dy > 0:
            minyifnegy = max(minyifnegy, y)
        else:
            maxyifplusy = min(maxyifplusy, y)
        if dz > 0:
            minzifnegz = max(minzifnegz, z)
        else:
            maxzifplusz = min(maxzifplusz, z)

    for i, j in combinations(range(len(hailstones)), 2):
        print('pair', i, j, len(hailstones))
        first = hailstones[i]
        second = hailstones[j]

        orderings = [[first, second], [second, first]]

        for at in range(1, 15):
            for a, b in orderings:
                for bt in range(at+1, at+15):
                    ax = a[0] + a[3] * at
                    ay = a[1] + a[4] * at
                    az = a[2] + a[5] * at

                    bx = b[0] + b[3] * bt
                    by = b[1] + b[4] * bt
                    bz = b[2] + b[5] * bt

                    dx = Fraction(bx-ax, bt-at)
                    dy = Fraction(by-ay, bt-at)
                    dz = Fraction(bz-az, bt-at)                    

                    rockx = Fraction(ax) - dx * at
                    rocky = Fraction(ay) - dy * at
                    rockz = Fraction(az) - dz * at

                    if dx > 0 and rockx > maxxifplusx:
                        continue
                    if dx < 0 and rockx < minxifnegx:
                        continue
                    if dy > 0 and rocky > maxyifplusy:
                        continue
                    if dy < 0 and rocky < minyifnegy:
                        continue
                    if dz > 0 and rockz > maxzifplusz:
                        continue
                    if dz < 0 and rockz < minzifnegz:
                        continue

                    if rockx != int(rockx):
                        continue
                    if rocky != int(rocky):
                        continue
                    if rockz != int(rockz):
                        continue

                    if collidesall(hailstones, (rockx, rocky, rockz, dx, dy, dz)):
                        return int(rockx) + int(rocky) + int(rockz)

    return None


def main():
    lines = []

    with open('24.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return (solve_a(lines), solve_b(lines))


if __name__ == '__main__':
    print(main())
