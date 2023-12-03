from aoc_prepare import PrepareAoc


def parse(inp):
    d = dict()
    numbers = list()
    symbols = dict()
    current_number = (0, list())
    for ridx, row in enumerate(inp.splitlines()):
        for cidx, c in enumerate(row + "."):
            if c.isdigit():
                current_number = (current_number[0] * 10 + int(c),
                                  current_number[1] + [(ridx, cidx)])
            else:
                if current_number[0] != 0:
                    numbers.append(current_number)
                    current_number = (0, list())
                if c != ".":
                    symbols[(ridx, cidx)] = c
    return numbers, symbols


def is_part_number(number_positions, symbol_positions):
    result = False
    for position in number_positions:
        for delta_r in range(-1, 2):
            for delta_c in range(-1, 2):
                if (position[0] + delta_r, position[1] + delta_c) in symbol_positions:
                    result = True
    return result

def part1(inp):
    numbers, symbols = parse(inp)
    symbol_positions = {pos for pos in symbols}
    return sum((number[0] for number in numbers if is_part_number(number[1], symbol_positions)))


def numbers_connected_to(numbers, symbol_position):
    result = list()
    for number, number_positions in numbers:
        connected = False
        for number_position in number_positions:
            for delta_r in range(-1, 2):
                for delta_c in range(-1, 2):
                    r, c = number_position[0] + delta_r, number_position[1] + delta_c
                    if (r, c) == symbol_position:
                        connected = True
        if connected:
            result.append(number)
    return result


def part2(inp):
    numbers, symbols = parse(inp)
    result = 0
    for symbol_position, symbol in symbols.items():
        if symbol != "*":
            continue
        part_numbers = numbers_connected_to(numbers, symbol_position)
        if len(part_numbers) == 2:
            result += (part_numbers[0] * part_numbers[1])
    return result


def test_1_1():
    assert part1("""467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..""")


def test_2_1():
    assert part2("""467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..""") == 467835


def main(inp):
    print("Part1:", part1(inp.strip()))
    print("Part2:", part2(inp.strip()))


if __name__ == "__main__":
    prep = PrepareAoc(2023, 3)
    main(prep.get_content())