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
    return [line.split() for line in lines]


def solve_line(springs, goal):
    @cache
    def inner_solve(springpos, goalpos, remaining):        
        if springpos == len(springs):
            return remaining == 0 and goalpos == len(goal) - 1

        take = 0
        if remaining:
            take = inner_solve(springpos + 1, goalpos, remaining - 1)
        
        skip = 0        
        if remaining == goal[goalpos]:
            skip = inner_solve(springpos + 1, goalpos, remaining)
        elif remaining == 0:
            if goalpos < len(goal) - 1:
                skip = inner_solve(springpos + 1, goalpos + 1, goal[goalpos + 1])
            else:
                skip = inner_solve(springpos + 1, goalpos, remaining)
        
        match springs[springpos]:
            case '.':
                return skip
            case '#':                
                return take
            case _:
                return skip + take
                
    return inner_solve(0, 0, goal[0])
print(solve_line('.??..??...?##.', [1, 1, 3]))
a = 2

def solve_a(lines):
    data = parse(lines)
    
    return sum(solve_line(d[0], ints(d[1])) for d in data)


def solve_b(lines):
    data = parse(lines)

    expand_springs = lambda springs: '?'.join(springs for _ in range(5))
    expand_config = lambda config: ints(config) * 5

    return sum(solve_line(expand_springs(d[0]), expand_config(d[1])) for d in data)


def main():
    lines = []

    with open('12.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return (solve_a(lines), solve_b(lines))


if __name__ == '__main__':
    print(main())
