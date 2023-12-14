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
    def solve(springpos, goalpos, remaining):        
        if springpos == len(springs):
            return remaining == 0 and goalpos == len(goal) - 1
        
        if remaining == 0 and goalpos == len(goal) - 1:
            return not any(c == '#' for c in springs[springpos:])

        take = 0 if not remaining else solve(springpos + 1, goalpos, remaining - 1)

        skip = \
            solve(springpos + 1, goalpos, remaining) if remaining == goal[goalpos] \
            else solve(springpos + 1, goalpos + 1, goal[goalpos + 1]) if not remaining \
            else 0
        
        match springs[springpos]:
            case '.':
                return skip
            case '#':                
                return take
            case '?':
                return skip + take
                
    return solve(0, 0, goal[0])
    

def solve_a(lines):
    data = parse(lines)
    
    return sum(solve_line(d[0], ints(d[1])) for d in data)


def solve_b(lines):
    data = parse(lines)

    expand_springs = lambda springs: '?'.join(springs for _ in range(5))
    expand_goal = lambda goal: ints(goal) * 5

    return sum(solve_line(expand_springs(d[0]), expand_goal(d[1])) for d in data)


def main():
    lines = []

    with open('12.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return (solve_a(lines), solve_b(lines))


if __name__ == '__main__':
    print(main())
