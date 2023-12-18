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
    data = []

    for line in lines:
        d = line.split()

        data.append((d[0], int(d[1]), d[2]))

    return data


def find_inside(points):
    miny = min(p[0] for p in points)
    maxy = max(p[0] for p in points)
    minx = min(p[1] for p in points)
    maxx = max(p[1] for p in points)

    for y, x in product(range(miny+1, maxy), range(minx+1, maxx)):
        if (y, x) in points:
            continue

        skips = 0

        for dx in range(x+1, maxx+1):
            if (y, dx) in points and not (y, dx-1) in points and not (y, x+1) in points:
                skips += 1

        if skips % 2:
            return y, x


def flood_fill(points, sy, sx):
    frontier = [(sy, sx)]

    for y, x in frontier:        
        if (y, x) in points:
            continue

        points.add((y, x))

        for ny, nx in neighs(y, x):
            if (ny, nx) not in points:
                frontier.append((ny, nx))
    

def solve_a(lines):
    vectors = {
        'R': (0, 1),
        'L': (0, -1),
        'U': (-1, 0),
        'D': (1, 0)
    }

    data = parse(lines)

    filled = {(0, 0)}
    y = 0
    x = 0

    for direction, length, _ in data:
        dy, dx = vectors[direction]

        for _ in range(length):
            y += dy
            x += dx
            filled.add((y, x))

    sy, sx = find_inside(filled)
    flood_fill(filled, sy, sx)

    return len(filled)


def solve_b(lines):
    oldrules = False

    vectors = {
        '0': (0, 1),
        '2': (0, -1),
        '3': (-1, 0),
        '1': (1, 0)
    }

    if oldrules:
        vectors = {
            'R': (0, 1),
            'L': (0, -1),
            'U': (-1, 0),
            'D': (1, 0)
        }

    data = parse(lines)
    
    y = 0
    x = 0
    miny = 0
    maxy = 0
    vertstrokes = []
    horistrokes = defaultdict(list)

    count = 0

    for i, d in enumerate(data):
        direction, length, colour = d
        dy=dx=-1

        if oldrules:
            dy, dx = vectors[direction]
        else:
            dy, dx = vectors[(colour[-2])]
            length = int(colour[2:-2], 16)

        prevdir = data[i-1][2][2]
        nextdir = data[(i+1) % len(data)][2][2]

        if oldrules:
            prevdir = data[i-1][0]
            nextdir = data[(i+1) % len(data)][0]
            
        plateau = dx != 0 and prevdir != nextdir

        if dy == 1:
            vertstrokes.append((x, y, y + length))
        if dy == -1:
            vertstrokes.append((x, y - length, y))
        if dx == 1:
            horistrokes[y].append((x, x + length, plateau))
        if dx == -1:
            horistrokes[y].append((x - length, x, plateau))
        
        y += dy * length
        x += dx * length

        miny = min(miny, y)
        maxy = max(maxy, y)

        # count += length - 1

    a = 22
    printed = set()

    for y in range(miny, maxy+1):
        hitting = [[x, True] for x, starty, endy in vertstrokes if between(y, starty, endy, False)]
        hitting.sort()
        
        contribution = 1
        inside = True

        for _, end, plateau in horistrokes[y]:
            for i in range(len(hitting)):
                if hitting[i][0] == end:
                    hitting[i][1] = plateau

        a = 22
        
        for i in range(1, len(hitting)):
            this = hitting[i]
            past = hitting[i-1]

            if inside or not this[1]:
                contribution += this[0] - past[0]
            
            if this[1]:
                inside = not inside

            # for linestart, lineend in horistrokes[y]:
            #     if linestart == pastx and lineend == thisx:
            #         if inside:
            #             contribution += lineend - linestart
            #         inside = not inside

        count += contribution

        if oldrules:
            print(y, maxy, hitting, contribution)
        else:
            # if len(hitting) > 3:
                # t = tuple([tuple(e) for e in hitting])
            t = tuple(e[1] for e in hitting)
            if t not in printed:
                print(y, maxy, hitting, contribution)
                printed.add(t)

    return count


def main():
    lines = []

    with open('18.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return (solve_a(lines), solve_b(lines))


if __name__ == '__main__':
    print(main())

# mytest   952402606509
# latest   952407216608
# corrtest 952408144115
# newstrat 952409011757
# +3run    952408655403
# +1run    952404622807
# +2run    952406639105