from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product

from algo import a_star, custsort, sssp
from helpers import adjacent, chunks, chunks_with_overlap, columns, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives, rays, rays_from_inside


def solve_a(lines):
    score = 0

    for line in lines:
        a, b = line.split('|')

        winners = set(ints(a.split(':')[1]))
        mine = set(ints(b))

        matches = len(winners&mine)

        if matches:
            score += 2**(matches-1)

    return score


def solve_b(lines):
    n = len(lines)
    cards = [1 for _ in range(n)]
    wins = []

    for line in lines:
        a, b = line.split('|')

        winners = set(ints(a.split(':')[1]))
        mine = set(ints(b))

        wins.append(len(winners&mine))
        
    for i in range(n):
        c = cards[i]
        w = wins[i]

        for x in range(i+1, i+1+w):
            if x < n:
                cards[x] += c
            else:
                break
    print(cards)
    return sum(cards)


def main():
    lines = []

    with open('4.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    print(solve_a(lines))
    print(solve_b(lines))


if __name__ == '__main__':
    main()
