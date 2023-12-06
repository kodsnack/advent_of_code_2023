from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product

from algo import a_star, custsort, merge_ranges, sssp
from helpers import adjacent, chunks, chunks_with_overlap, columns, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives, rays, rays_from_inside


def parse(lines):
    groups = grouped_lines(lines)

    seeds = ints(groups[0][0])
    conversions = []

    for group in groups[1:]:
        rules = []

        for row in group[1:]:
            deststart, sourcestart, length = map(int, row.split())
            rules.append((sourcestart, sourcestart+length-1, deststart))

        rules.sort()

        conversions.append(rules)

    return seeds, conversions
    

def solve_a(lines):
    seeds, conversions = parse(lines)

    locations = []

    for seed in seeds:
        val = seed

        for conversion in conversions:

            for sourcestart, sourceend, deststart in conversion:
                if sourcestart <= val <= sourceend:
                    diff = val-sourcestart
                    val = deststart+diff
                    break

        locations.append(val)

    return min(locations)


def solve_b(lines):
    seedranges, conversions = parse(lines)
    
    level = 0
    ranges = []

    for i in range(0, len(seedranges), 2):
        start, length = seedranges[i:i+2]
        ranges.append([start, start+length-1])

    while level < 7:        
        candidates = []

        for start, end in ranges:
            prevend = -1

            for sourcestart, sourceend, deststart in conversions[level]:
                gapstart = max(start, prevend+1)
                gapend = min(end, sourcestart-1)

                if gapend >= gapstart:
                    candidates.append((gapstart, gapend))

                overlapstart = max(start, sourcestart)
                overlapend = min(end, sourceend)

                if overlapend >= overlapstart:
                    diff = overlapstart-sourcestart
                    length = overlapend-overlapstart+1
                    candidates.append((deststart+diff, deststart+diff+length-1))

                prevend = sourceend

            postgapstart = max(prevend+1, start)
            
            if end >= postgapstart:
                candidates.append((postgapstart, end))
        
        ranges = merge_ranges(candidates)

        level += 1

    return min(r[0] for r in ranges)


def main():
    lines = []

    with open('5.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    print(solve_a(lines))
    print(solve_b(lines))

    return (solve_a(lines), solve_b(lines))


if __name__ == '__main__':
    print(main())