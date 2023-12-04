def solve_part_one(input_data):
    sum = 0
    for row in input_data.splitlines():
        row = row.strip()
        first = None
        last = None
        for char in row:
            if char.isdigit():
                if first is None:
                    first = int(char)
                else:
                    last = int(char)
        if last is None:
            last = first
        rowsum = int(10 * first + last)
        sum += rowsum
    return sum


def solve_part_two(input_data):
    numbers = [
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
        "ten",
    ]
    sum = 0

    for row in input_data.splitlines():
        row = row.strip()
        start = None
        first = None
        last = None
        firstnr = None
        lastnr = None
        for num in numbers:
            if num in row:
                startnr = [i for i in range(len(row)) if row.startswith(num, i)]
                for start in startnr:
                    position = numbers.index(num) + 1
                    if first is None:
                        first = start
                        firstnr = position
                    elif start < first:
                        first = start
                        firstnr = position
                    if last is None:
                        last = start
                        lastnr = position
                    elif start > last:
                        last = start
                        lastnr = position
        for ix, char in enumerate(row):
            if char.isdigit():
                val = int(char)
                if first is None:
                    firstnr = val
                    first = ix
                elif ix < first:
                    firstnr = val
                    first = ix
                if last is None:
                    lastnr = val
                    last = ix
                elif ix > last:
                    lastnr = val
                    last = ix

        if first == last:
            tmp = firstnr * 10 + firstnr
        else:
            tmp = firstnr * 10 + lastnr
        sum += tmp
    return sum


if __name__ == "__main__":
    with open("input.txt", "r") as file:
        input_data = file.read()

    part_one_solution = solve_part_one(input_data)
    print(f"Part One Solution: {part_one_solution}")

    part_two_solution = solve_part_two(input_data)
    print(f"Part Two Solution: {part_two_solution}")
