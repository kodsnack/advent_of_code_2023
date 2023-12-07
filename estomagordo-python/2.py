from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product

from algo import a_star, custsort, sssp
from helpers import adjacent, chunks, chunks_with_overlap, columns, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives, rays, rays_from_inside


def parse(lines):
    games = {}

    for line in lines:
        game = line.split(':')
        id = ints(game[0])[0]
        pulls = []

        moves = game[1].split()

        for i in range(0, len(moves), 2):
            pulls.append((int(moves[i]), moves[i+1].rstrip(',;')))

        games[id] = pulls

    return games


def solve_a(lines):
    maxred = 12
    maxgreen = 13
    maxblue = 14

    count = 0

    games = parse(lines)

    for id, pulls in games.items():
        possible = True

        for num, colour in pulls:
            if colour == 'red':
                if num > maxred:
                    possible = False
            if colour == 'blue':
                if num > maxblue:
                    possible = False
            if colour == 'green':
                if num > maxgreen:
                    possible = False

        if possible:
            count += id

    return count


def solve_b(lines):
    count = 0

    games = parse(lines)

    for pulls in games.values():
        red = 0
        blue = 0
        green = 0

        for num, colour in pulls:
            if colour == 'red':
                red = max(red, num)
            if colour == 'blue':
                blue = max(blue, num)
            if colour == 'green':
                green = max(green, num)

        count += red * blue * green

    return count


def main():
    lines = []

    with open('2.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return (solve_a(lines), solve_b(lines))


if __name__ == '__main__':
    print(main())