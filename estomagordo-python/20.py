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
    graph = {}

    for line in lines:
        parts = line.split()
        label = parts[0]

        module_type = 0 if label[0] == '%' else 1 if label[0] == '&' else 2
        name = label if module_type == 2 else label[1:]
        destinations = []

        for p in parts[2:]:
            destinations.append(p.rstrip(','))

        graph[name] = [module_type, destinations, 0, {}]

    for name in graph.keys():
        for destination in graph[name][1]:            
            if destination in graph and graph[destination][0] == 1:
                graph[destination][3][name] = 0

    return graph


def cycle(graph, key_inputs=set()):
    counts = [0, 0]
    key_inputs_set = set()
    pulses = [('button', 'broadcaster', 0)]

    for sender, receiver, pulse in pulses:
        counts[pulse] += 1

        if receiver not in graph:
            continue           

        module_type, destinations, _, _ = graph[receiver]

        if module_type == 0:
            if pulse == 0:
                graph[receiver][2] = 1 - graph[receiver][2]
                outsignal = graph[receiver][2]

                for d in destinations:
                    pulses.append((receiver, d, outsignal))

        if module_type == 1:
            graph[receiver][3][sender] = pulse
            outpulse = 0 if all(v == 1 for v in graph[receiver][3].values()) else 1

            for d in destinations:
                pulses.append((receiver, d, outpulse))

            if outpulse == 1 and receiver in key_inputs:
                key_inputs_set.add(receiver)

        if module_type == 2:
            for d in destinations:
                pulses.append((receiver, d, pulse))

    return counts, key_inputs_set
    

def solve_a(lines):
    graph = parse(lines)
    counts = [0, 0]
    
    for _ in range(1000):
        lohi, _ = cycle(graph)
        lo, hi = lohi
        counts[0] += lo
        counts[1] += hi

    return counts[0] * counts[1]


def solve_b(lines):
    graph = parse(lines)
    presses = 0
    
    rx_input = ''

    for k, v in graph.items():
        for d in v[1]:
            if d == 'rx':
                rx_input = k                

    key_inputs = {}

    for k, v in graph.items():
        for d in v[1]:
            if d == rx_input:
                key_inputs[k]= 0

    while True:
        presses += 1
        _, key_inputs_set = cycle(graph, {k for k in key_inputs.keys()})

        for key_input in key_inputs_set:
            if key_inputs[key_input] == 0:
                key_inputs[key_input] = presses

            if not any(v == 0 for v in key_inputs.values()):
                return lcm(*key_inputs.values())


def main():
    lines = []

    with open('20.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return (solve_a(lines), solve_b(lines))


if __name__ == '__main__':
    print(main())
