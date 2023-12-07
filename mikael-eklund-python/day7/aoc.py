from collections import Counter


def hand_val(hand):
    nohits = len(set(hand)) == len(hand)
    cards_counts = Counter(hand)
    pairs = sum(count == 2 for count in cards_counts.values())
    tok = any(count == 3 for count in cards_counts.values())
    four = any(count == 4 for count in cards_counts.values())
    five = any(count == 5 for count in cards_counts.values())
    if nohits:
        return 0
    if not tok and pairs == 1:
        return 1
    if not five and pairs == 2:
        return 2
    if tok and pairs == 0:
        return 3
    if tok and pairs == 1:
        return 4
    if four:
        return 5
    if five:
        return 6


def hand_val2(hand):
    nohits = len(set(hand)) == len(hand)
    cards_counts = Counter(hand)
    pairs = sum(count == 2 for count in cards_counts.values())
    tok = any(count == 3 for count in cards_counts.values())
    four = any(count == 4 for count in cards_counts.values())
    five = any(count == 5 for count in cards_counts.values())
    joker = hand.count("J")
    if nohits:
        if joker == 0:
            return 0
        else:
            return joker
    if not tok and pairs == 1:
        if joker == 0:
            return 1
        else:
            return 3
    if not five and pairs == 2:
        if joker == 0:
            return 2
        if joker == 1:
            return 4
        else:
            return 5
    if tok and pairs == 0:
        if joker == 0:
            return 3
        else:
            return 5
    if tok and pairs == 1:
        if joker == 0:
            return 4
        else:
            return 6
    if four:
        if joker == 0:
            return 5
        else:
            return 6
    if five:
        return 6


def compare_cards(card1, card2):
    cards = {
        "A": 14,
        "K": 13,
        "Q": 12,
        "J": 11,
        "T": 10,
        "9": 9,
        "8": 8,
        "7": 7,
        "6": 6,
        "5": 5,
        "4": 4,
        "3": 3,
        "2": 2,
    }
    for i in range(5):
        if cards[card1[i]] > cards[card2[i]]:
            return 1
        elif cards[card1[i]] < cards[card2[i]]:
            return -1
    return 0


def compare_cards2(card1, card2):
    cards = {
        "A": 14,
        "K": 13,
        "Q": 12,
        "T": 11,
        "9": 10,
        "8": 9,
        "7": 8,
        "6": 7,
        "5": 6,
        "4": 5,
        "3": 4,
        "2": 3,
        "J": 2,
    }
    for i in range(5):
        if cards[card1[i]] > cards[card2[i]]:
            return 1
        elif cards[card1[i]] < cards[card2[i]]:
            return -1
    return 0


def flip_cards(hands, x, y):
    list_hands = list(hands)
    list_hands[x], list_hands[y] = list_hands[y], list_hands[x]
    flipped_cards = tuple(list_hands)
    return flipped_cards


def solve_part_one(input_data):
    hands = []
    sum = 0
    for row in input_data.splitlines():
        hand = row.split(" ")[0].strip()
        bid = int(row.split(" ")[1].strip())
        value = hand_val(hand)
        hands.append([hand, bid, value])
    hands.sort(key=lambda x: x[2], reverse=True)
    flipped = True
    while flipped:
        flipped = False
        for ix, hand in enumerate(hands):
            if ix < len(hands) - 1:
                if hand[2] == hands[ix + 1][2]:
                    check_size = compare_cards(hand[0], hands[ix + 1][0])
                    if check_size == -1:
                        flipped_cards = flip_cards(hands, ix, ix + 1)
                        flipped = True
            if flipped is True:
                hands = flipped_cards
    hands = hands[::-1]
    for ix, hand in enumerate(hands):
        sum += hand[1] * (ix + 1)
    return sum


def solve_part_two(input_data):
    hands = []
    sum = 0
    for row in input_data.splitlines():
        hand = row.split(" ")[0].strip()
        bid = int(row.split(" ")[1].strip())
        value = hand_val2(hand)
        hands.append([hand, bid, value])
    hands.sort(key=lambda x: x[2], reverse=True)
    flipped = True
    while flipped:
        flipped = False
        for ix, hand in enumerate(hands):
            if ix < len(hands) - 1:
                if hand[2] == hands[ix + 1][2]:
                    check_size = compare_cards2(hand[0], hands[ix + 1][0])
                    if check_size == -1:
                        flipped_cards = flip_cards(hands, ix, ix + 1)
                        flipped = True
            if flipped is True:
                hands = flipped_cards
    hands = hands[::-1]
    for ix, hand in enumerate(hands):
        sum += hand[1] * (ix + 1)
    return sum


if __name__ == "__main__":
    with open("input.txt", "r") as file:
        input_data = file.read()

    part_one_solution = solve_part_one(input_data)
    print(f"Part One Solution: {part_one_solution}")

    part_two_solution = solve_part_two(input_data)
    print(f"Part Two Solution: {part_two_solution}")
