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
    data = []

    for d in lines[0].split(','):
        if '-' in d:
            data.append((d, d[:-1], -1))
        else:
            label, sval = d.split('=')
            data.append((d, label, int(sval)))

    return data


def score(seq):
    return reduce(lambda a, b: (a + b) * 17 % 256, map(ord, seq), 0)


def solve_a(lines):
    data = parse(lines)

    return sum(score(d[0]) for d in data)


def solve_b(lines):
    data = parse(lines)

    boxes = [{} for _ in range(256)]

    for _, label, length in data:
        boxpos = score(label)
        box = boxes[boxpos]

        if length == -1:
            if label in box:
                del box[label]
        else:
            box[label] = length

    return sum((i+1) * (j+1) * length for i, box in enumerate(boxes) for j, length in enumerate(box.values()))


def main():
    lines = []

    with open('15.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return (solve_a(lines), solve_b(lines))


if __name__ == '__main__':
    print(main())
