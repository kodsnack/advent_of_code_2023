from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from math import ceil, comb, factorial, gcd, isclose, lcm

from algo import a_star, custsort, merge_ranges, sssp
from constants import EPSILON
from helpers import adjacent, chunks, chunks_with_overlap, columns, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, overlap, positives, rays, rays_from_inside


def cardvalue(card):
    match card:
        case 'T':
            return 10
        case 'J':
            return 11
        case 'Q':
            return 12
        case 'K':
            return 13
        case 'A':
            return 14
        case _:
            return int(card)


def score_hand(cards):
    c = Counter(cards)

    match len(c):
        case 1:
            return 6
        case 2:
            return 4 + any(v == 4 for v in c.values())
        case 3:
            return 2 + any(v == 3 for v in c.values())
        case 4:
            return 1
        case 5:
            return 0


def hand(cards):    
    best = score_hand(cards)

    if best == 6 or '1' not in cards:
        return best
    
    most_common_non_joker = Counter(card for card in cards if card != '1').most_common(1)[0][0]    

    return score_hand(cards.replace('1', most_common_non_joker))


def parse(lines):
    hands = []

    for line in lines:
        cards, bid = line.split()
        strength = hand(cards)
        values = [cardvalue(card) for card in cards]
        hands.append((strength, values, int(bid), cards))

    return sorted(hands)


def solve_a(lines):
    hands = parse(lines)

    return sum((i+1) * hands[i][2] for i in range(len(hands)))


def solve_b(lines):
    hands = parse([line.replace('J', '1') for line in lines])

    return sum((i+1) * hands[i][2] for i in range(len(hands)))


def main():
    lines = []

    with open('7.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return (solve_a(lines), solve_b(lines))


if __name__ == '__main__':
    print(main())