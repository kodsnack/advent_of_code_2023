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

    import graphviz

    g = graphviz.Graph('g')
    # g.graph_attr['dpi'] = '1000'
    colors = ['red', 'green', 'blue', 'pink', 'orange', 'brown', 'yellow', 'purple', 'magenta', 'bisque', 'brown2', 'darkgreen', 'darkolivegreen', 'darkkhaki', 'gold']

    from random import choice

    left = ['dhl', 'xvp', 'nzn']
    right = []

    for k in left:
        for e in graph[k]:
            right.append(e)

    right = ['pbq', 'zpc', 'vfs']

    for k, v in graph.items():
        for e in v:
            if k < e:
                if k in left and e in right:
                    print(k, e)

    ans = []

    for k in graph.keys():
        color = 'red' if k in left else 'green' if k in right else 'blue'
        g.node(k, k, fillcolor=color, style='filled')

    for k, v in graph.items():
        for e in v:
            if k < e:
                # color = 'red' if k in interesting or e in interesting else 'black'
                # color = choice(colors)
                # color = 'red' if (k[0] == 'n' and k[1] == 'z') else 'blue'
                color = 'red' if k in left and e in right else 'blue'
                g.edge(k, e, f'{k} <-> {e}', color=color)

    g.render('25', view=True)
    
    return graph
    

def solve_a(lines):
    graph = parse(lines)

    return len(graph)


def solve_b(lines):
    data = parse(lines)

    return None


def main():
    lines = []

    with open('25.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return (solve_a(lines), solve_b(lines))


if __name__ == '__main__':
    print(main())
