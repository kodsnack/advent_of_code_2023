from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product

from algo import a_star, custsort, sssp
from helpers import adjacent, chunks, chunks_with_overlap, columns, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives, rays, rays_from_inside


def parse(lines):
    times = ints(lines[0])
    distances = ints(lines[1])

    return times, distances
    

def solve_a(lines):
    times, distances = parse(lines)

    total = 1
    n = len(times)

    for i in range(n):
        t = times[i]
        d = distances[i]

        ways = 0

        for x in range(1, t):
            remaining = t-x
            went = x*remaining

            if went > d:
                ways += 1

        total *= ways

    return total


def solve_b(lines):
    times, distances = parse(lines)

    time = int(''.join(str(t) for t in times))
    distance = int(''.join(str(d) for d in distances))

    ways = 0

    for x in range(1, time):
        remaining = time-x
        went = x*remaining

        if went > distance:
            ways += 1

    return ways

def main():
    lines = []

    with open('6.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return (solve_a(lines), solve_b(lines))


if __name__ == '__main__':
    print(main())
