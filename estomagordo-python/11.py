from bisect import bisect, bisect_left, bisect_right
from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from math import ceil, comb, factorial, gcd, isclose, lcm

from algo import a_star, custsort, merge_ranges, sssp
from constants import EPSILON
from helpers import adjacent, between, chunks, chunks_with_overlap, columns, digits, dimensions, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, overlap, positives, rays, rays_from_inside, sum_of_differences, words


def solve(lines, spacing):
    def list_by_dimension(sequence, limit):
        empty = 0
        l = []

        for i in range(limit):
            galaxy_count = sequence[i].count('#')

            if galaxy_count == 0:
                empty += 1

            for _ in range(galaxy_count):
                l.append(i + empty * spacing)

        return l

    h, w = dimensions(lines)
    
    ys = list_by_dimension(lines, h)
    xs = list_by_dimension(columns(lines), w)

    return sum_of_differences(ys) + sum_of_differences(xs)
    

def solve_a(lines):
    return solve(lines, 1)


def solve_b(lines):
    return solve(lines, 999999)


def main():
    lines = []

    with open('11.txt') as f:
        for line in f.readlines():
            lines.append(line.rstrip())
            
    return (solve_a(lines), solve_b(lines))


if __name__ == '__main__':
    print(main())