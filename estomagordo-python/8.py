from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from math import ceil, comb, factorial, gcd, isclose, lcm

from algo import a_star, custsort, merge_ranges, sssp
from constants import EPSILON
from helpers import adjacent, chunks, chunks_with_overlap, columns, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, overlap, positives, rays, rays_from_inside


def parse(lines):
    inst = lines[0].rstrip()

    graph = {}

    for line in lines[2:]:
        parts = line.split()

        start = parts[0]
        l = parts[2][1:-1]
        r = parts[3][:-1]

        graph[start] = (l, r)

    return inst, graph
    

def solve_a(lines):
    return 1
    inst, graph = parse(lines)

    node = 'AAA'
    steps = 0
    pos = 0

    while node != 'ZZZ':
        move = inst[pos % len(inst)]

        node = graph[node][0 if move == 'L' else 1]
        steps += 1
        pos += 1

    return steps


def solve_b(lines):
    inst, graph = parse(lines)

    nodes = [[node, node] for node in graph.keys() if node[-1] == 'A']
    firsttook = {}
    diff = {}
    steps = 0
    pos = 0
    # znodes = [node for node in graph.keys() if node[-1] == 'Z']

    while any(node[0][-1] != 'Z' for node in nodes):
        if len(diff) == len(nodes):
            print(lcm(*list(val for val in diff.values())))
        move = inst[pos % len(inst)]

        for i, nodepair in enumerate(nodes):
            node, orignode = nodepair

            if node[-1] == 'Z':
                if orignode not in firsttook:
                    print('first')
                    print(firsttook)
                    print()
                    print(diff)
                    firsttook[orignode] = steps
                elif orignode not in diff:
                    diff[orignode] = steps - firsttook[orignode]
                    print('second')
                    print(firsttook)
                    print()
                    print(diff)

            nodes[i] = [graph[node][0 if move == 'L' else 1], orignode]
        
        steps += 1
        pos += 1


    return steps


    print(anodes, znodes)
    anodesteps = []
    
    n = len(anodes)

    for anode in anodes:
        znodesfound = set()
        zsteps = []
        steps = 0
        pos = 0
        node = anode

        while len(znodesfound) < n:
            if node in znodes and node not in znodesfound:
                print(anode, node)
                znodesfound.add(node)
                zsteps.append(steps)

            move = inst[pos % len(inst)]
            node = graph[node][0 if move == 'L' else 1]
            steps += 1
            pos += 1

        anodesteps.append(zsteps)

    return anodesteps


def main():
    lines = []

    with open('8.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return (solve_a(lines), solve_b(lines))


if __name__ == '__main__':
    print(main())
