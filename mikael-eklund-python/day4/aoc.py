def solve_part_one(input_data):
    sums = 0
    for row in input_data.splitlines():
        card = row.split(":")[0].strip()
        card = card.split(" ")[1]
        numbers = row.split(":")[1].strip()
        wins = numbers.split("|")[0].strip()
        wins = wins.split(" ")
        yours = numbers.split("|")[1].strip()
        yours = yours.split(" ")
        points = 0
        for win in wins:
            if not win == "":
                if win in yours:
                    if points == 0:
                        points = 1
                    else:
                        points = points * 2
        sums += points
        points = 0
    return sums


def solve_part_two(input_data):
    cards = {}
    length = len(input_data.splitlines())
    for i in range(1, length + 1):
        cards[i] = 1
    for row in input_data.splitlines():
        card = row.split(":")[0].strip()
        card = int(card.split(" ")[-1])
        numbers = row.split(":")[1].strip()
        wins = numbers.split("|")[0].strip()
        wins = wins.split(" ")
        yours = numbers.split("|")[1].strip()
        yours = yours.split(" ")
        points = 0
        if card in cards:
            value = cards[card]
        else:
            value = 0
        points = 0
        for win in wins:
            if not win == "":
                if win in yours:
                    points += 1
        for i in range(card + 1, card + points + 1):
            if i <= length:
                if i in cards:
                    cards[i] += value
        summa = sum(cards.values())
    return summa


if __name__ == "__main__":
    with open("input.txt", "r") as file:
        input_data = file.read()

    part_one_solution = solve_part_one(input_data)
    print(f"Part One Solution: {part_one_solution}")

    part_two_solution = solve_part_two(input_data)
    print(f"Part Two Solution: {part_two_solution}")
