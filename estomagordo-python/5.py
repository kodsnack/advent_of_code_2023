from collections import Counter, defaultdict, deque
from functools import cache, reduce
from heapq import heapify, heappop, heappush
from itertools import combinations, permutations, product

from algo import a_star, custsort, sssp
from helpers import adjacent, chunks, chunks_with_overlap, columns, digits, distance, distance_sq, eight_neighs, eight_neighs_bounded, grouped_lines, ints, manhattan, multall, n_neighs, neighs, neighs_bounded, positives, rays, rays_from_inside


def parse(lines):
    groups = grouped_lines(lines)

    # seeds = set()
    # seed_to_soil = {}
    # soil_to_fertilizer = {}
    # fertilizer_to_water = {}
    # water_to_light = {}
    # light_to_temperature = {}
    # temperature_to_humidity = {}
    # humidity_to_location = {}

    # for s in ints(groups[0]):
    #     seeds.add(s)

    seeds = ints(groups[0][0])
    conversions = []

    for group in groups[1:]:
        rules = []

        for row in group[1:]:
            deststart, sourcestart, length = map(int, row.split())
            rules.append((sourcestart, sourcestart+length-1, deststart, deststart+length-1))

        rules.sort()

        conversions.append(rules)

    return seeds, conversions

    

def solve_a(lines):
    seeds, conversions = parse(lines)

    locations = []

    for seed in seeds:
        val = seed

        for conversion in conversions:

            for sourcestart, sourceend, deststart, destend in conversion:
                if sourcestart <= val <= sourceend:
                    diff = val-sourcestart
                    val = deststart+diff
                    break

        locations.append(val)

    print(locations)
    return min(locations)


def solve_b(lines):
    seedranges, conversions = parse(lines)

    chunks = []

    for i in range(0, len(seedranges), 2):
        start, length = seedranges[i:i+2]
        chunks.append((0, start, start+length-1, start, length))

    bestgoal = 10**100 
    maxlevel = 0
    passes = 0

    while chunks:
        level, start, end, origstart, length = chunks.pop()
        passes += 1
        maxlevel = max(maxlevel, level)
        if passes % 10000000 == 0:
            print(passes, len(chunks), level, maxlevel, bestgoal)
        if level == 7:
            if start < bestgoal:
                bestgoal = start
                print('goal', start)
            continue

        if start < conversions[level][0][0]:
            lastbefore = min(conversions[level][0][0]-1, end)
            diff = lastbefore-start

            chunks.append((level+1, start, lastbefore, origstart, diff+1))

        for sourcestart, sourceend, deststart, destend in conversions[level]:
            overlapstart = max(start, sourcestart)
            overlapend = min(end, sourceend)
            diff = overlapend-overlapstart

            if overlapstart <= overlapend:
                fromdiff = overlapstart-start
                todiff = overlapstart-sourcestart

                chunks.append((level+1, deststart+todiff, deststart+todiff+diff, origstart+fromdiff, diff+1))

        prevend = conversions[level][0][1]

        for sourcestart, sourceend, deststart, destend in conversions[level][1:]:
            gapstart = max(prevend+1, start)
            gapend = min(sourcestart-1, end)

            if gapstart <= gapend:
                gapdiff = gapstart-start
                chunks.append((level+1, gapstart, gapend, gapdiff, gapend-gapstart+1))

        if end > conversions[level][-1][1]:
            firstafter = max(conversions[level][-1][1]+1, start)
            diff = end-firstafter

            chunks.append((level+1, firstafter, end, origstart+diff, diff+1))


    return bestgoal


def main():
    lines = []

    with open('5.txt') as f:
        for line in f.readlines():
            lines.append(line)
            
    print(solve_a(lines))
    print(solve_b(lines))


if __name__ == '__main__':
    main()

# 601583464 too high
# 130185120 too high
# 25134997 too high