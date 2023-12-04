from os import path
from sys import argv

program_file = lambda day: f"""from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product

from algo import a_star, custsort, sssp
from helpers import adjacent, chunks, chunks_with_overlap, columns, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives, rays, rays_from_inside


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
            
    print(solve_a(lines))
    print(solve_b(lines))


if __name__ == '__main__':
    main()
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