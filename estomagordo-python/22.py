from bisect import bisect_left, bisect_right
from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from math import ceil, comb, factorial, gcd, isclose, lcm

from algo import a_star, custsort, merge_ranges, sssp
from constants import EPSILON, HUGE
from helpers import adjacent, between, chunks, chunks_with_overlap, columns, digits, dimensions, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, overlap, positives, rays, rays_from_inside, words


def parse(lines):
    return [ints(line) for line in lines]
    

def solve_a(lines):
    bricks = parse(lines)

    bricks.sort(key=lambda brick: min(brick[2], brick[5]))

    occupied = {}

    while True:
        anymoved = False

        for i, brick in enumerate(bricks):
            lowest = min(brick[2], brick[5])

            while lowest > 1:
                moveable = True

                for y in range(min(brick[1], brick[4]), max(brick[1], brick[4])+1):
                    if not moveable:
                        break
                    for x in range(min(brick[0], brick[3]), max(brick[0], brick[3])+1):
                        if (x, y, lowest-1) in occupied:
                            moveable = False
                            break

                if not moveable:
                    break

                anymoved = True                
                
                brick[2] -= 1                
                brick[5] -= 1
                lowest -= 1

            highest = max(brick[2], brick[5])

            for y in range(min(brick[1], brick[4]), max(brick[1], brick[4])+1):                
                for x in range(min(brick[0], brick[3]), max(brick[0], brick[3])+1):
                    if (x, y, highest+1) in occupied and occupied[(x, y, highest+1)] == i:
                        del occupied[(x, y, highest+1)]
                    for z in range(min(brick[2], brick[5]), max(brick[2], brick[5])+1):
                        occupied[(x, y, z)] = i

            bricks[i] = brick

        if not anymoved:
            break

    supporting = defaultdict(set)
    supported = defaultdict(set)

    for i, brick in enumerate(bricks):
        for y in range(min(brick[1], brick[4]), max(brick[1], brick[4])+1):                
            for x in range(min(brick[0], brick[3]), max(brick[0], brick[3])+1):
                if (x, y, max(brick[2], brick[5])+1) in occupied:
                    j = occupied[(x, y, max(brick[2], brick[5])+1)]
                    if i == j:
                        print('panic')
                    supporting[i].add(j)
                    supported[j].add(i)

    count = 0

    for i, brick in enumerate(bricks):
        if min(brick[2], brick[5]) == 1 and i in supported:
            print('panic')

    # print(len(occupied))

    # print(min(brick[2] for brick in bricks))
    # print(min(brick[5] for brick in bricks))
    # print(min(coord[2] for coord in occupied.keys()))

    for i in range(len(bricks)):
        if i not in supporting or not supporting[i] or len(supporting[i]) == 0: # fugly
            if i not in supported and min(bricks[i][2], bricks[i][5]) > 1:
                print('panic')
            count += 1
            continue

        if all(len(supported[j]) > 1 for j in supporting[i]):
            count += 1

    return count


def solve_b(lines):
    bricks = parse(lines)

    bricks.sort(key=lambda brick: min(brick[2], brick[5]))

    occupied = {}

    while True:
        anymoved = False

        for i, brick in enumerate(bricks):
            lowest = min(brick[2], brick[5])

            while lowest > 1:
                moveable = True

                for y in range(min(brick[1], brick[4]), max(brick[1], brick[4])+1):
                    if not moveable:
                        break
                    for x in range(min(brick[0], brick[3]), max(brick[0], brick[3])+1):
                        if (x, y, lowest-1) in occupied:
                            moveable = False
                            break

                if not moveable:
                    break

                anymoved = True                
                
                brick[2] -= 1                
                brick[5] -= 1
                lowest -= 1

            highest = max(brick[2], brick[5])

            for y in range(min(brick[1], brick[4]), max(brick[1], brick[4])+1):                
                for x in range(min(brick[0], brick[3]), max(brick[0], brick[3])+1):
                    if (x, y, highest+1) in occupied and occupied[(x, y, highest+1)] == i:
                        del occupied[(x, y, highest+1)]
                    for z in range(min(brick[2], brick[5]), max(brick[2], brick[5])+1):
                        occupied[(x, y, z)] = i

            bricks[i] = brick

        if not anymoved:
            break

    supporting = defaultdict(set)
    supported = defaultdict(set)

    for i, brick in enumerate(bricks):
        for y in range(min(brick[1], brick[4]), max(brick[1], brick[4])+1):                
            for x in range(min(brick[0], brick[3]), max(brick[0], brick[3])+1):
                if (x, y, max(brick[2], brick[5])+1) in occupied:
                    j = occupied[(x, y, max(brick[2], brick[5])+1)]
                    if i == j:
                        print('panic')
                    supporting[i].add(j)
                    supported[j].add(i)
    
    def chain_reaction(i, s):
        if i not in supporting:
            return s
        
        for j in supporting[i]:
            if not supported[j] - s:
                s.add(j)
                s |= chain_reaction(j, s)
        
        return s        
    
    for i in range(len(bricks)):
        print(i, chain_reaction(i, {i}), len(chain_reaction(i, {i})))
    
    return sum(len(chain_reaction(i, {i})) for i in range(len(bricks))) - len(bricks)
    
    # count = 0

    # for i, brick in enumerate(bricks):
    #     if min(brick[2], brick[5]) == 1 and i in supported:
    #         print('panic')

    # # print(len(occupied))

    # # print(min(brick[2] for brick in bricks))
    # # print(min(brick[5] for brick in bricks))
    # # print(min(coord[2] for coord in occupied.keys()))

    # for i in range(len(bricks)):
    #     if i not in supporting or not supporting[i] or len(supporting[i]) == 0: # fugly
    #         if i not in supported and min(bricks[i][2], bricks[i][5]) > 1:
    #             print('panic')
    #         count += 1
    #         continue

    #     if all(len(supported[j]) > 1 for j in supporting[i]):
    #         count += 1

    # return count


def main():
    lines = []

    with open('22.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return (solve_a(lines), solve_b(lines))


if __name__ == '__main__':
    print(main())

# a 709 731