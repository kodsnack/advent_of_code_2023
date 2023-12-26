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


def are_parallel(dsx, dsy, dsz, drx, dry, drz):
    return False

    return dsx == drx or dsy == dry or dsz == drz


def collides_in_future(stone, rock):
    sx, sy, sz, dsx, dsy, dsz = stone
    rx, ry, rz, drx, dry, drz = rock

    stricttx = True
    strictty = True
    stricttz = True

    if are_parallel(dsx, dsy, dsz, drx, dry, drz):
        return False
    
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

# collides_in_future([19, 13, 30, -2, 1, -2], [Fraction(24), Fraction(13), Fraction(10), Fraction(-3), Fraction(1), Fraction(2)])
    
    # if dsx > 0:
    #     if drx > 0:
    #         if sx > rx:
    #             if dsx > drx:
    #                 return False
    #         elif drx > dsx:
    #             return False
    #     elif sx > rx:
    #         return False
    # else:
    #     if drx < 0:
    #         if sx < rx:
    #             if dsx < drx:
    #                 return False
    #         elif drx < dsx:
    #             return False
    #     elif sx < rx:
    #         return False
        
    # return True


def is_solution(hailstones, rock):
    return all(collides_in_future(stone, rock) for stone in hailstones)


def gauss_jordan(equations):
    h, w = dimensions(equations)
    used = set()

    for pos in range(w-1):
        for i, equation in enumerate(equations):
            val = equation[pos]

            if i in used or val == Fraction(0):
                continue

            used.add(i)

            for j in range(w):
                equations[i][j] /= val

            for j in range(h):
                if j == i:
                    continue

                factor = -equations[j][pos]

                for k in range(w):
                    equations[j][k] += factor * equations[i][k]

            break

    return equations


def find_solution(dx, dy, x1, x2, y1, y2, dx1, dx2, dy1, dy2):
    equations = [
        [1, 0, dx - dx1, 0, x1],
        [1, 0, 0, dx - dx2, x2],
        [0, 1, dy - dy1, 0, y1],
        [0, 1, 0, dy - dy2, y2]
    ]

    equations = [[Fraction(val) for val in row] for row in equations]

    reduced = gauss_jordan(equations)

    x = y = t1 = t2 = 0

    for i in range(len(reduced)):
        if reduced[i][0] == Fraction(1):
            x = reduced[i][-1]
        if reduced[i][1] == Fraction(1):
            y = reduced[i][-1]
        if reduced[i][2] == Fraction(1):
            t1 = reduced[i][-1]
        if reduced[i][3] == Fraction(1):
            t2 = reduced[i][-1]

    return x, y, t1, t2
                

# print(find_solution())
# print(gauss_jordan([
#     [1, 0, -1, 0, 19],
#     [1, 0, 0, -2, 18],
#     [0, 1, 0, 0, 13],
#     [0, 1, 0, 2, 19]
# ]))
# a = 22
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

    span = 300

    for dx in range(-span, span):
        for dy in range(-span, span):
            x, y, t1, t2 = find_solution(Fraction(dx), Fraction(dy), x1, x2, y1, y2, dx1, dx2, dy1, dy2)

            if t1 < 0 or t2 < 0:
                continue

            z1 = hailstones[0][2] + hailstones[0][5] * t1
            z2 = hailstones[1][2] + hailstones[1][5] * t2

            z = dz = Fraction(0)

            if t1 == t2:
                continue

            # print('yo')

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
                print(x, y, z, dx, dy, dz, t1, t2)
                return x + y + z
            
    return

    # maxxifplusx = HUGE
    # minxifnegx = UNHUGE
    # maxyifplusy = HUGE
    # minyifnegy = UNHUGE
    # maxzifplusz = HUGE
    # minzifnegz = UNHUGE

    # for x, y, z, dx, dy, dz in hailstones:
    #     if dx > 0:
    #         minxifnegx = max(minxifnegx, x)
    #     else:
    #         maxxifplusx = min(maxxifplusx, x)
    #     if dy > 0:
    #         minyifnegy = max(minyifnegy, y)
    #     else:
    #         maxyifplusy = min(maxyifplusy, y)
    #     if dz > 0:
    #         minzifnegz = max(minzifnegz, z)
    #     else:
    #         maxzifplusz = min(maxzifplusz, z)

    closest = min(manhattan(a, b) for a, b in combinations(hailstones, 2))

    for i, j in combinations(range(len(hailstones)), 2):
        print('pair', i, j, len(hailstones))
        first = hailstones[i]
        second = hailstones[j]

        orderings = [[first, second], [second, first]]

        for at in range(1, 50):
            for a, b in orderings:
                for bt in range(at+1, at+50):
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

                    if is_solution(hailstones, (rockx, rocky, rockz, dx, dy, dz)):
                        return int(rockx) + int(rocky) + int(rockz)
                    
                    continue

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

# 806413550299304 too low
# 856642398547748