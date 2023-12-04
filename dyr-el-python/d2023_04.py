from aoc_prepare import PrepareAoc


def parse_line(line):
    split = False
    before = list()
    after = list()
    for word in line.split(' '):
        if word in ["Card", ":", ""]:
            continue
        elif word[-1]== ":":
            card_no = int(word[:-1])
        elif word == "|":
            split = True
        else:
            if split:
                after.append(int(word.strip()))
            else:
                before.append(int(word.strip()))
    return card_no, before, after


def part1(inp):
    total = 0
    for line in inp.splitlines():
        _, winning, you = parse_line(line)
        tot = len(set(winning) & set(you))
        if tot == 0:
            continue
        total += 2 ** (tot-1)
    return int(total)


def part2(inp):
    cards = {1: 1}
    for line in inp.splitlines():
        card_no, winning, you = parse_line(line)
        cards[card_no] = cards.get(card_no, 1)
        for i in range(card_no + 1, card_no + 1 + len(set(winning) & set(you))):
            cards[i] = cards.get(i, 1) + cards[card_no]
    return sum(cards.values())


def test_1_1():
    assert 13 == part1("""Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11""")


def test_2_1():
    assert 30 == part2("""Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11""")


def main(inp):
    print("Part1:", part1(inp.strip()))
    print("Part2:", part2(inp.strip()))


if __name__ == "__main__":
    prep = PrepareAoc(2023, 4)
    main(prep.get_content())