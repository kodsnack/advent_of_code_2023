from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product
from math import ceil, comb, factorial, gcd, isclose, lcm

from algo import a_star, custsort, merge_ranges, sssp
from constants import EPSILON
from helpers import adjacent, chunks, chunks_with_overlap, columns, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, overlap, positives, rays, rays_from_inside


def cardvalue(card):
    if card.isdigit():
        return int(card)
    
    if card == 'T':
        return 10
    if card == 'J':
        return 11
    if card == 'Q':
        return 12
    if card == 'K':
        return 13
    return 14


def cardvalue_b(card):
    if card.isdigit():
        return int(card)
    
    if card == 'T':
        return 10
    if card == 'J':
        return 1
    if card == 'Q':
        return 12
    if card == 'K':
        return 13
    return 14


def hand(cards):
    c = Counter(cards)
    
    if len(c) == 1:
        return 6
    
    if len(c) == 5:
        return 0
    
    if len(c) == 4:
        return 1
    
    if len(c) == 2:
        if any(v == 4 for v in c.values()):
            return 5
        return 4
    
    if any(v == 3 for v in c.values()):
        return 3
    
    return 2


def hand_b(cards):
    best = hand(cards)

    jpositions = []
    
    for i, c in enumerate(cards):
        if c == 'J':
            jpositions.append(i)

    for selections in product('23456789TQKA', repeat=len(jpositions)):
        dcards = list(cards)

        for i, selection in enumerate(selections):
            dcards[jpositions[i]] = selection

        best = max(best, hand(dcards))

    return best


def parse(lines):
    hands = []

    for line in lines:
        cards, bid = line.split()
        strength = hand(cards)
        values = [cardvalue(card) for card in cards]
        hands.append((strength, values, int(bid), cards))

    return sorted(hands)

    
def parse_b(lines):
    hands = []

    for line in lines:
        cards, bid = line.split()
        strength = hand_b(cards)
        values = [cardvalue_b(card) for card in cards]
        hands.append((strength, values, int(bid), cards))

    return sorted(hands)


def solve_a(lines):
    hands = parse(lines)

    score = 0

    for i in range(len(hands)):
        score += (i+1) * hands[i][2]

    return score


def solve_b(lines):
    hands = parse_b(lines)

    score = 0

    for i in range(len(hands)):
        score += (i+1) * hands[i][2]

    return score


def main():
    lines = []

    with open('7.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    return (solve_a(lines), solve_b(lines))


if __name__ == '__main__':
    print(main())

# 248437797