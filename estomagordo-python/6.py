from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product

from algo import a_star, custsort, sssp
from constants import EPSILON
from helpers import adjacent, chunks, chunks_with_overlap, columns, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives, rays, rays_from_inside


def parse(lines):
    times = ints(lines[0])
    distances = ints(lines[1])

    return times, distances


def ways(time, distance):
    halfway = time / 2.0
    root_distance = (time**2 / 4.0 - distance)**0.5

    a = int(halfway - root_distance + EPSILON)
    b = int(halfway + root_distance - EPSILON)

    return b - a
    

def solve_a(lines):
    times, distances = parse(lines)

    return multall(ways(t, d) for t, d in zip(times, distances))


def solve_b(lines):
    time = int(''.join(str(t) for t in ints(lines[0])))
    distance = int(''.join(str(d) for d in ints(lines[1])))

    return ways(time, distance)


def main():
    lines = []

    with open('6.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return (solve_a(lines), solve_b(lines))


if __name__ == '__main__':
    print(main())
