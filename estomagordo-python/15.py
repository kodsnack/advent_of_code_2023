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

    boxes = [[] for _ in range(256)]

    for _, label, length in data:
        boxpos = score(label)
        box = boxes[boxpos]

        if length == -1:
            for i in range(len(box)):
                if box[i][0] == label:
                    boxes[boxpos] = box[:i] + box[i+1:]
                    break
        else:
            found = False

            for i, lense in enumerate(box):
                lab = lense[0]

                if lab == label:
                    box[i][1] = length
                    found = True
                    break

            if not found:
                box.append([label, length])

    s = 0

    for i, box in enumerate(boxes):
        for j, lense in enumerate(box):
            s += (i+1) * (j+1) * (lense[1])

    return s


def main():
    lines = []

    with open('15.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return (solve_a(lines), solve_b(lines))


if __name__ == '__main__':
    print(main())
