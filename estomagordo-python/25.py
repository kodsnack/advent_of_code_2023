from bisect import bisect_left, bisect_right
from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from math import ceil, comb, factorial, gcd, isclose, lcm

from algo import a_star, custsort, merge_ranges, sssp
from constants import EPSILON, HUGE
from helpers import adjacent, between, chunks, chunks_with_overlap, columns, digits, dimensions, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, overlap, positives, rays, rays_from_inside, words


def find_critical_edges(graph):
    edge_frequency = Counter()

    for start in graph.keys():
        preceeding = {}
        frontier = [(start, None)]

        for node, prev in frontier:
            if node in preceeding:
                continue

            preceeding[node] = prev

            for next in graph[node]:
                if next not in preceeding:
                    frontier.append((next, node))


        for node in preceeding.keys():
            while preceeding[node]:
                prev = preceeding[node]
                edge_frequency[(min(node, prev), max(node, prev))] += 1
                node = prev

    return {a: b for a, b in [p[0] for p in edge_frequency.most_common(3)]}


def parse(lines):
    graph = defaultdict(list)

    for line in lines:
        parts = line.split()

        a = parts[0][:-1]

        for part in parts[1:]:
            graph[a].append(part)
            graph[part].append(a)

    critical_edges = find_critical_edges(graph)
    
    return graph, critical_edges
    

def size(graph, start):
    seen = set()
    frontier = [start]

    for node in frontier:
        seen.add(node)

        for neighbour in graph[node]:
            if neighbour not in seen:
                frontier.append(neighbour)

    return len(seen)


def solve(lines):
    graph, critical_edges = parse(lines)
    critical_nodes = list(critical_edges.keys()) + list(critical_edges.values())

    for key in critical_nodes:
        graph[key] = [node for node in graph[key] if node not in critical_nodes]

    return size(graph, list(critical_edges.items())[0][0]) * size(graph, list(critical_edges.items())[0][1])


def main():
    lines = []

    with open('25.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return solve(lines)


if __name__ == '__main__':
    print(main())
