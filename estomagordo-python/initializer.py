from os import path
from sys import argv

program_file = lambda day: f"""from bisect import bisect_left, bisect_right
from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from math import ceil, comb, factorial, gcd, isclose, lcm

from algo import a_star, custsort, merge_ranges, sssp
from constants import EPSILON, HUGE, UNHUGE
from helpers import adjacent, between, chunks, chunks_with_overlap, columns, digits, dimensions, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, overlap, positives, rays, rays_from_inside, words


def parse(lines):
    return None
    

def solve_a(lines):
    data = parse(lines)

    return None


def solve_b(lines):
    data = parse(lines)

    return None


def main():
    lines = []

    with open('{day}.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return (solve_a(lines), solve_b(lines))


if __name__ == '__main__':
    print(main())
"""

if __name__ == '__main__':
    day = argv[1]
    
    program = f'{day}.py'
    inp = f'{day}.txt'

    if not path.isfile(program):
        with open(program, 'w') as g:
            g.write(program_file(day))
    if not path.isfile(inp):
        with open(inp, 'w') as g:
            g.write('')