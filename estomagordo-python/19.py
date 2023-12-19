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
    wfs, ps = grouped_lines(lines)

    workflows = {}
    parts = []

    for wf in wfs:
        label, ins = wf.split('{')
        insts = ins[:-1].split(',')
        i = []

        for inst in insts:
            if not ints(inst):
                i.append((inst,))
            else:
                resource = inst[0]
                less = inst[1] == '<'
                num = ints(inst)[0]
                target = inst.split(':')[1]

                i.append((resource, less, num, target))

        workflows[label] = i

    for p in ps:
        contents = {}

        for part in p[1:-1].split(','):
            u = part.split('=')
            contents[u[0]] = int(u[1])

        parts.append(contents)
    
    return workflows, parts
    

def solve_a(lines):
    workflows, parts = parse(lines)

    def evaluate(p):
        flow = 'in'

        while flow not in ('R', 'A'):
            workflow = workflows[flow]

            for step in workflow:
                if len(step) == 1:
                    flow = step[0]
                    break

                resource, less, num, target = step                   

                if resource in p:
                    if less:
                        if p[resource] < num:
                            flow = target
                            break
                    elif p[resource] > num:
                        flow = target
                        break

        if flow == 'A':
            return sum(p.values())
        
        return 0

    return sum(evaluate(p) for p in parts)


def solve_b(lines):
    workflows = parse(lines)[0]
    total = 0

    frontier = [('in', {'x': [1, 4000], 'm': [1, 4000], 'a': [1, 4000], 's': [1, 4000]})]

    for label, d in frontier:
        if label == 'A':
            total += multall(v[1]+1-v[0] for v in d.values())
            continue

        if label == 'R':
            continue
        
        workflow = workflows[label]

        for step in workflow:
            if len(step) == 1:
                frontier.append((step[0], dict(d)))
            else:
                resource, less, num, target = step

                lo, hi = d[resource]

                if less:
                    if lo < num:
                        newd = dict(d)
                        newd[resource] = [lo, num-1]
                        frontier.append((target, newd))
                        d[resource] = [num, hi]
                else:
                    if hi > num:
                        newd = dict(d)
                        newd[resource] = [num+1, hi]
                        frontier.append((target,newd))
                        d[resource] = [lo, num]

    return total            


def main():
    lines = []

    with open('19.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return (solve_a(lines), solve_b(lines))


if __name__ == '__main__':
    print(main())
