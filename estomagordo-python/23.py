from bisect import bisect_left, bisect_right
from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from math import ceil, comb, factorial, gcd, isclose, lcm

from algo import a_star, custsort, merge_ranges, sssp
from constants import EPSILON, HUGE, UNHUGE
from helpers import adjacent, between, chunks, chunks_with_overlap, columns, digits, dimensions, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, junctions, manhattan, multall, n_neighs, neighs, neighs_bounded, overlap, positives, rays, rays_from_inside, words


def parse(lines, abide_by_arrows=True):
    h, w = dimensions(lines)

    sy = 0
    sx = [x for x in range(w) if lines[0][x] == '.'][0]
    gy = h-1
    gx = [x for x in range(w) if lines[h-1][x] == '.'][0]

    intersections = junctions(lines, '#')
    nodes = intersections + [(sy, sx), (gy, gx)]
    
    graph = defaultdict(dict)

    for ny, nx in nodes:
        frontier = [(0, ny, nx)]
        seen = {(ny, nx)}

        for steps, y, x in frontier:
            if (y, x) in nodes and (y != ny or x != nx):
                graph[(ny, nx)][(y, x)] = steps
                continue

            for yy, xx in neighs_bounded(y, x, 0, h-1, 0, w-1):
                c = lines[yy][xx]

                if c == '#':
                    continue

                if (yy, xx) in seen:
                    continue

                if abide_by_arrows and c != '.':
                    dy = yy-y
                    dx = xx-x

                    matching = (dy == 1 and c == 'v') or (dy == -1 and c == '^') or (dx == 1 and c == '>') or (dx == -1 and c == '<')

                    if matching:
                        seen.add((yy, xx))
                        seen.add((yy+dy, xx+dx))
                        frontier.append((steps+2, yy+dy, xx+dx))

                    continue

                seen.add((yy, xx))
                frontier.append((steps+1, yy, xx))

    return graph, sy, sx


def longest_walk(graph, sy, sx, gy):
    def walk(node, seen):
        if node[0] == gy:
            return 0
        
        val = UNHUGE

        for next in graph[node]:
            if next in seen:
                continue

            seen.add(next)
            val = max(val, graph[node][next] + walk(next, seen))
            seen.remove(next)

        return val

    return walk((sy, sx), {(sy, sx)})
    

def solve_a(lines):
    h, _ = dimensions(lines)
    graph, sy, sx = parse(lines)

    return longest_walk(graph, sy, sx, h-1)


def solve_b(lines):
    h, _ = dimensions(lines)
    graph, sy, sx = parse(lines, False)

    return longest_walk(graph, sy, sx, h-1)


def main():
    lines = []

    with open('23.txt') as f:
        for line in f.readlines():
            lines.append(line.rstrip())
            
    return (solve_a(lines), solve_b(lines))


if __name__ == '__main__':
    print(main())