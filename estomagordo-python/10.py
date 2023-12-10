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
    h = len(lines)
    w = len(lines[0])

    origh = h
    origw = w

    ystretchgraph = [[('.', -1, -1) for _ in range(w)]]

    for y, line in enumerate(lines):
        stretchrow = []

        for x, c in enumerate(line):
            if c in '|LJ':
                stretchrow.append(('|', -1, -1))
            else:
                stretchrow.append(('.', -1, -1))        

        ystretchgraph.append(stretchrow)

        row = []

        for x, c in enumerate(line):
            row.append((c, y, x))

        ystretchgraph.append(row)

    ystretchgraph.append([('.', -1, -1) for _ in range(w)])

    fullgraph = []

    for row in ystretchgraph:
        newrow = [['.', -1, -1]]

        for c, y, x in row:
            if c in '-J7':
                newrow.append(['-', -1, -1])
            else:
                newrow.append(['.', -1, -1])
            newrow.append((c, y, x))

        newrow.append(['.', -1, -1])
        
        fullgraph.append(newrow)

    h = len(fullgraph)
    w = len(fullgraph[0])

    # for y, row in enumerate(fullgraph):
    #     for x, tile in enumerate(row):
    #         if x > 0 and fullgraph[y][x-1][0] == '-' and y < h-1 and fullgraph[y+1][x][0] == '|':
    #             fullgraph[y][x][0] = '7'
    #         if x > 0 and fullgraph[y][x-1][0] == '-' and y > 0 and fullgraph[y-1][x][0] == '|':
    #             fullgraph[y][x][0] = 'J'
    
    for y, row in enumerate(fullgraph):
        print(''.join(r[0] for r in row))  

    sy = -1
    sx = -1

    for y, row in enumerate(fullgraph):
        for x, tile in enumerate(row):
            if tile[0] == 'S':
                sy = y
                sx = x

    seen = {(sy, sx): 0}
    loopseen = {(sy, sx)}
    frontier = []

    if sy > 0 and fullgraph[sy-1][sx][0] in '|7F':
        frontier.append((1, sy-1, sx))        
    if sy < h-1 and fullgraph[sy+1][sx][0] in '|LJ':
        frontier.append((1, sy+1, sx))
    if sx > 0 and fullgraph[sy][sx-1][0] in '-LF':
        frontier.append((1, sy, sx+1))        
    if sx < w-1 and fullgraph[sy][sx+1][0] in '-J7':
        frontier.append((1, sy, sx+1))

    for steps, y, x in frontier:
        if (y, x) in seen:
            continue

        seen[(y, x)] = steps

        origy, origx = fullgraph[y][x][1:]
        
        if origy > -1 and origx > -1:
            loopseen.add((origy, origx))

        c = fullgraph[y][x][0]
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

    # print()
    
    # for y in range(origh):
    #     row = []

    #     for x in range(origw):
    #         row.append('*' if (y, x) in loopseen else '.')

    #     print(row)
    
    frontier = []

    for y in range(h):
        if fullgraph[y][0][0] == '.':
            frontier.append((y, 0))
        if fullgraph[y][w-1][0] == '.':
            frontier.append((y, w-1))

    for x in range(w):
        if fullgraph[0][x][0] == '.':
            frontier.append((0, x))
        if fullgraph[h-1][x][0] == '.':
            frontier.append((h-1, x))
    
    genuine_outside = set()    
    outside = set()

    for y, x in frontier:
        if (y, x) in outside:
            continue

        outside.add((y, x))

        ry, rx = fullgraph[y][x][1:]

        if ry > -1 and rx > -1:
            genuine_outside.add((ry, rx))

        for ny, nx in neighs_bounded(y, x, 0, h-1, 0, w-1):
            if (ny, nx) in outside or (ny, nx) in seen:
                continue

            frontier.append((ny, nx))

    print()
    count = 0
    
    for y in range(origh):
        row = []

        for x in range(origw):
            if (y, x) in loopseen:
                # row.append(lines[y][x])
                row.append('.')
            elif (y, x) in genuine_outside:
                # row.append('O')
                row.append('.')
            else:
                row.append('I')
                count += 1

        print(''.join(row))
    
    print(count)

    return origh * origw - len(loopseen) - len(genuine_outside)


def main():
    lines = []

    with open('10.txt') as f:
        for line in f.readlines():
            lines.append(line.rstrip())
            
    return (solve_a(lines), solve_b(lines))


if __name__ == '__main__':
    print(main())