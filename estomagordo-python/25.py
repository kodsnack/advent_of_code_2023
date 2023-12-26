from bisect import bisect_left, bisect_right
from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from math import ceil, comb, factorial, gcd, isclose, lcm

from algo import a_star, custsort, merge_ranges, sssp
from constants import EPSILON, HUGE
from helpers import adjacent, between, chunks, chunks_with_overlap, columns, digits, dimensions, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, overlap, positives, rays, rays_from_inside, words


def parse(lines):
    graph = defaultdict(list)

    for line in lines:
        parts = line.split()

        a = parts[0][:-1]

        for part in parts[1:]:
            graph[a].append(part)
            graph[part].append(a)

    left = ['dhl', 'xvp', 'nzn']
    right = ['pbq', 'zpc', 'vfs']
    
    return graph, left, right
    

def size(graph, start):
    seen = set()
    frontier = [start]

    for node in frontier:
        seen.add(node)

        for neighbour in graph[node]:
            if neighbour not in seen:
                frontier.append(neighbour)

    return len(seen)


def solve_a(lines):
    graph, left, right = parse(lines)

    for key in left + right:
        graph[key] = [node for node in graph[key] if node not in left + right]

    return size(graph, left[0]) * size(graph, right[0])


def main():
    lines = []

    with open('25.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return solve_a(lines)


if __name__ == '__main__':
    print(main())
