from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product

from algo import a_star, custsort, sssp
from helpers import adjacent, chunks, chunks_with_overlap, columns, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives, rays, rays_from_inside


def solve_a(lines):
    numbers = {}
    symbols = set()

    h = len(lines)
    w = len(lines[0])
    currnum = ''

    for y in range(h):
        for x in range(w):
            c = lines[y][x]

            if c.isdigit():
                currnum += c
                continue

            if currnum:
                numlen = len(currnum)
                l = []

                fx = w if x == 0 else x
                fy = y-1 if x == 0 else y

                for dx in range(fx-numlen, fx):
                    l.append((fy, dx))

                numbers[tuple(l)] = int(currnum)

                currnum = ''

            if c == '.':
                continue            

            symbols.add((y, x))

    total = 0

    for cells, number in numbers.items():
        isadjacent = False

        for y, x in cells:
            for ny, nx in eight_neighs(y, x):
                if (ny, nx) in symbols:
                    isadjacent = True

        if isadjacent:
            total += number

        # if number < 10:print(number, isadjacent, y, x)

    return total



def solve_b(lines):
    numbers = {}
    gears = set()

    h = len(lines)
    w = len(lines[0])
    currnum = ''

    for y in range(h):
        for x in range(w):
            c = lines[y][x]

            if c.isdigit():
                currnum += c
                continue

            if currnum:
                numlen = len(currnum)
                l = []

                fx = w if x == 0 else x
                fy = y-1 if x == 0 else y

                for dx in range(fx-numlen, fx):
                    l.append((fy, dx))

                numbers[tuple(l)] = int(currnum)

                currnum = ''

            if c == '*':
                gears.add((y, x))

    total = 0

    for y, x in gears:
        nums = []

        for cells, number in numbers.items():
            isadjacent = False

            for cy, cx in cells:
                for ny, nx in eight_neighs(cy, cx):
                    if (ny, nx) == (y, x):
                        isadjacent = True

            if isadjacent:
                nums.append(number)

        if len(nums) == 2:
            total += nums[0] * nums[1]

    return total


def main():
    lines = []

    with open('3.txt') as f:
        for line in f.readlines():
            lines.append(line.rstrip())
            
    print(solve_a(lines))
    print(solve_b(lines))


if __name__ == '__main__':
    main()