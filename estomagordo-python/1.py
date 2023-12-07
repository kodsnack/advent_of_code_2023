from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product

from algo import a_star, custsort, sssp
from helpers import adjacent, chunks, chunks_with_overlap, columns, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives, rays, rays_from_inside


def solve_a(lines):
    return sum(10 * digits(line)[0] + digits(line)[-1] for line in lines)


def solve_b(lines):
    written = [
        'zero',
        'one',
        'two',
        'three',
        'four',
        'five',
        'six',
        'seven',
        'eight',
        'nine',
    ]
    
    def evaluate_pos(line, pos):
        if line[pos].isdigit():
            return int(line[pos])
        
        for i, w in enumerate(written):
            if pos + len(w) <= len(line) and line[pos:pos+len(w)] == w and i > 0:
                return i
            
    def evaluate_line(line):
        digits = [evaluate_pos(line, pos) for pos in range(len(line)) if evaluate_pos(line, pos)]

        return 10 * digits[0] + digits[-1]

    return sum(evaluate_line(line) for line in lines)


def main():
    lines = []

    with open('1.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return (solve_a(lines), solve_b(lines))


if __name__ == '__main__':
    print(main())