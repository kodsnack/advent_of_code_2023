from aoc_prepare import PrepareAoc


from collections import Counter


value1 = {c:val for val, c in enumerate("23456789TJQKA")}
value2 = {c:val for val, c in enumerate("J23456789TQKA")}


def map_values(inp, values):
    return [values[c] for c in inp]


def type_value(hand):
    hand = Counter(hand)
    tp = hand.most_common()
    if tp[0][1] == 5:
        return 7
    elif tp[0][1] == 4:
        return 6
    elif tp[0][1] == 3 and tp[1][1] == 2:
        return 5
    elif tp[0][1] == 3:
        return 4
    elif tp[0][1] == 2 and tp[1][1] == 2:
        return 3
    elif tp[0][1] ==2:
        return 2
    return 1


def parse1(inp):
    l = list()
    for line in inp.splitlines():
        hand, bid = line.split()
        hand = map_values(hand, value1)
        hand_value = type_value(hand)
        bid = int(bid)
        l.append((hand_value, hand, bid))
    return l


def parse2(inp):
    l = list()
    for line in inp.splitlines():
        hand, bid = line.split()
        hand = map_values(hand, value2)
        max_hand_type_value = max((type_value(([zero if card == 0 else card for card in hand]))
                                   for zero in range(0, 13)))
        bid = int(bid)
        l.append((max_hand_type_value, hand, bid))
    return l


def part1(inp):
    result = parse1(inp)
    result.sort()
    return sum((bid[2] * rank for rank, bid in enumerate(result, start=1)))


def part2(inp):
    result = parse2(inp)
    result.sort()
    return sum((bid[2] * rank for rank, bid in enumerate(result, start=1)))


def test_1_1():
    assert 6440 == part1("""32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483""")



def test_2_1():
    assert 5905 == part2("""32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483""")


def main(inp):
    print("Part1:", part1(inp.strip()))
    print("Part2:", part2(inp.strip()))


if __name__ == "__main__":
    prep = PrepareAoc(2023, 7)
    main(prep.get_content())