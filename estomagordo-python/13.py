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


def score_pattern(pattern, orig_score=-1):
    cols = columns(pattern)

    for i, col in enumerate(cols[:-1]):
        if col == cols[i+1]:
            could = True
            for j in range(1, i+1):
                if i + j + 1 < len(cols) and cols[i-j] != cols[i+j+1]:
                    could = False
            if could and orig_score != i+1:
                return i + 1
        
    for i, row in enumerate(pattern[:-1]):
        if row == pattern[i+1]:
            could = True
            for j in range(1, i+1):
                if i + j + 1 < len(pattern) and pattern[i-j] != pattern[i+j+1]:
                    could = False
            if could and orig_score != 100 * (i+1):
                return 100 * (i + 1)
        
    return - 10**10
    

def solve_a(lines):
    patterns = parse(lines)

    return sum(score_pattern(pattern) for pattern in patterns)


def solve_b(lines):
    patterns = parse(lines)

    total = 0

    for i, pattern in enumerate(patterns):
        l = [list(line) for line in pattern]
        orig_score = score_pattern(pattern)
        done = False

        for y in range(len(l)):
            if done:
                break
            for x in range(len(l[0])):
                if l[y][x] == '.':
                    l[y][x] = '#'
                    score = score_pattern(l, orig_score)
                    if score > 0:
                        total += score
                        done = True
                        break
                    l[y][x] = '.'
                else:
                    l[y][x] = '.'
                    score = score_pattern(l, orig_score)
                    if score > 0:
                        total += score
                        done = True
                        break
                    l[y][x] = '#'

    return total


def main():
    lines = []

    with open('13.txt') as f:
        for line in f.readlines():
            lines.append(line.rstrip())
            
    return (solve_a(lines), solve_b(lines))


if __name__ == '__main__':
    print(main())

# 31974