from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product

from algo import a_star, custsort, sssp
from helpers import adjacent, chunks, chunks_with_overlap, columns, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives, rays, rays_from_inside


def solve_a(lines):
    i = [ints(c) for c in lines]

    s = 0

    # for j in i:
    #     s += 10 * j[0] + j[-1]

    for line in lines:
        digs = []

        for c in line:
            if c.isdigit():
                digs.append(int(c))

        if digs:
            s += 10 * digs[0] + digs[-1]

    return s


def solve_b(lines):
    i = [ints(c) for c in lines]

    s = 0

    # for j in i:
    #     s += 10 * j[0] + j[-1]

    for line in lines:
        digs = []
        linlen = len(line)

        for i, c in enumerate(line):
            if c.isdigit():
                digs.append(int(c))
            else:
                if i + 3 <= linlen and line[i:i+3] == 'one':
                    digs.append(1)
                if i + 3 <= linlen and line[i:i+3] == 'two':
                    digs.append(2)
                if i + 3 <= linlen and line[i:i+3] == 'six':
                    digs.append(6)
                if i + 4 <= linlen and line[i:i+4] == 'four':
                    digs.append(4)
                if i + 4 <= linlen and line[i:i+4] == 'five':
                    digs.append(5)
                if i + 4 <= linlen and line[i:i+4] == 'nine':
                    digs.append(9)
                if i + 5 <= linlen and line[i:i+5] == 'three':
                    digs.append(3)
                if i + 5 <= linlen and line[i:i+5] == 'seven':
                    digs.append(7)
                if i + 5 <= linlen and line[i:i+5] == 'eight':
                    digs.append(8)            

        print(digs)

        s += 10 * digs[0] + digs[-1]

    return s


def main():
    lines = []

    with open('1.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    print(solve_a(lines))
    print(solve_b(lines))


if __name__ == '__main__':
    main()

# 55372