from bisect import bisect, bisect_left, bisect_right
from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from math import ceil, comb, factorial, gcd, isclose, lcm

from algo import a_star, custsort, merge_ranges, sssp
from constants import EPSILON
from helpers import adjacent, between, chunks, chunks_with_overlap, columns, digits, dimensions, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, overlap, positives, rays, rays_from_inside, words


def parse(lines):
    return grouped_lines(lines)


def score_rows(pattern, orig_score=-1):        
    for i, row in enumerate(pattern[:-1]):
        if row == pattern[i+1]:
            could = True
            for j in range(1, i+1):
                if i + j + 1 < len(pattern) and pattern[i-j] != pattern[i+j+1]:
                    could = False
            if could and orig_score != i + 1:
                return i + 1
        
    return -10**10    


def score_pattern(pattern, orig_score=-1):
    return max(100 * score_rows(pattern, orig_score / 100), score_rows(columns(pattern), orig_score))
    

def solve_a(lines):
    patterns = parse(lines)

    return sum(score_pattern(pattern) for pattern in patterns)


def solve_b(lines):
    patterns = parse(lines)

    total = 0

    for pattern in patterns:
        l = [list(line) for line in pattern]
        orig_score = score_pattern(pattern)
        replacement = { '.': '#', '#': '.'}
        h, w = dimensions(l)
        done = False

        for y, x in product(range(h), range(w)):
            if done:
                break

            l[y][x] = replacement[l[y][x]]

            score = score_pattern(l, orig_score)
            
            if score > 0:
                total += score
                done = True

            l[y][x] = replacement[l[y][x]]

    return total


def main():
    lines = []

    with open('13.txt') as f:
        for line in f.readlines():
            lines.append(line.rstrip())
            
    return (solve_a(lines), solve_b(lines))


if __name__ == '__main__':
    print(main())