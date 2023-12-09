from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product

from algo import a_star, custsort, sssp
from helpers import adjacent, chunks, chunks_with_overlap, columns, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives, rays, rays_from_inside


def parse(lines):
    h = len(lines)
    w = len(lines[0])

    numbers = {}
    symbols = {}
    numbers_found = 0
    currnum = ''

    for y in range(h):
        for x in range(w):
            c = lines[y][x]

            if c.isdigit():
                currnum += c
                continue

            if currnum:
                numlen = len(currnum)

                fx = w if x == 0 else x
                fy = y-1 if x == 0 else y

                for dx in range(fx-numlen, fx):
                    numbers[(fy, dx)] = (int(currnum), numbers_found)

                numbers_found += 1
                currnum = ''

            if c == '.':
                continue            

            symbols[(y, x)] = c

    return numbers, symbols


def solve_a(lines):
    numbers, symbols = parse(lines)

    found = set()
    total = 0

    for y, x in symbols.keys():
        for ny, nx in eight_neighs(y, x):
            if (ny, nx) in numbers:
                val, i = numbers[(ny, nx)]

                if i not in found:
                    found.add(i)
                    total += val

    return total


def solve_b(lines):
    numbers, symbols = parse(lines)
    gears = [k for k, v in symbols.items() if v == '*']

    total = 0

    for y, x in gears:
        nums = set()

        for ny, nx in eight_neighs(y, x):
            if (ny, nx) in numbers:
                nums.add(numbers[(ny, nx)])

        if len(nums) == 2:
            total += multall(num[0] for num in nums)

    return total


def main():
    lines = []

    with open('3.txt') as f:
        for line in f.readlines():
            lines.append(line.rstrip())
            
    return (solve_a(lines), solve_b(lines))


if __name__ == '__main__':
    print(main())