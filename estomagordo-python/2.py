from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product

from algo import a_star, custsort, sssp
from helpers import adjacent, chunks, chunks_with_overlap, columns, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives, rays, rays_from_inside


def solve_a(lines):
    maxred = 12
    maxgreen = 13
    maxblue = 14

    count = 0

    for line in lines:
        game = line.split(':')
        id = ints(game[0])[0]

        guesses = game[1].split(';')

        possible = True

        for guess in guesses:
            parts = guess.split()            

            for i, part in enumerate(parts):
                if part.isdigit():
                    num = int(part)
                    colour = parts[i+1]

                    if colour in ['red','red,','red;']:
                        if num > maxred:
                            possible = False
                    if colour in ['blue','blue,','blue;']:
                        if num > maxblue:
                            possible = False
                    if colour in ['green','green,','green;']:
                        if num > maxgreen:
                            possible = False

        if possible:
            count += id

    return count


def solve_b(lines):
    count = 0

    for line in lines:
        game = line.split(':')
        id = ints(game[0])[0]
        red = 0
        blue = 0
        green = 0

        guesses = game[1].split(';')

        for guess in guesses:
            parts = guess.split()            

            for i, part in enumerate(parts):
                if part.isdigit():
                    num = int(part)
                    colour = parts[i+1]

                    if colour in ['red','red,','red;']:
                        red = max(red, num)
                    if colour in ['blue','blue,','blue;']:
                        blue = max(blue, num)
                    if colour in ['green','green,','green;']:
                        green = max(green, num)

        count += red*blue*green

    return count


def main():
    lines = []

    with open('2.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    print(solve_a(lines))
    print(solve_b(lines))


if __name__ == '__main__':
    main()

# 100 3374