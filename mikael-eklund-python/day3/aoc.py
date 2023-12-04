import re


def find_positions(string, number):
    pattern = r"\b" + re.escape(str(number)) + r"\b"
    matches = re.finditer(pattern, string)
    positions = [match.start() for match in matches]
    return positions


def solve_part_one(input_data):
    summa = 0
    grid = []
    fnum = []
    y = 0
    for row in input_data.splitlines():
        grid.append(row.strip())
    for ix, row in enumerate(grid):
        numbers = set(re.findall(r"\d+", row))
        for num in numbers:
            allnum = find_positions(row, num)
            for xstart in allnum:
                check = True
                xend = xstart + len(num) - 1
                for ix1, row1 in enumerate(grid):
                    diff = y - ix1
                    if 1 >= diff >= -1:
                        symbols = re.findall(r"[^0-9\.]+", row1)
                        for sym in symbols:
                            allsym = [
                                i for i in range(len(row1)) if row1.startswith(sym, i)
                            ]
                            for xstart1 in allsym:
                                found = False
                                if xstart - 1 <= xstart1 <= xend + 1:
                                    found = True
                                if found:
                                    if check:
                                        fnum.append(int(num))
                                        check = False
        y += 1
    summa = sum(fnum)
    return summa


def solve_part_two(input_data):
    grid = []
    fnum = []
    syms = {}
    y = 0
    for row in input_data.splitlines():
        grid.append(row.strip())
    for ix, row in enumerate(grid):
        numbers = set(re.findall(r"\d+", row))
        for num in numbers:
            allnum = find_positions(row, num)
            for xstart in allnum:
                check = True
                xend = xstart + len(num) - 1
                for ix1, row1 in enumerate(grid):
                    diff = y - ix1
                    if 1 >= diff >= -1:
                        symbols = re.findall(r"[^0-9\.]+", row1)
                        for sym in symbols:
                            allsym = [
                                i for i in range(len(row1)) if row1.startswith(sym, i)
                            ]
                            for xstart1 in allsym:
                                sums = 0
                                numval = 1
                                found = False
                                if xstart - 1 <= xstart1 <= xend + 1:
                                    found = True
                                if found:
                                    if check:
                                        fnum.append(int(num))
                                        check = False
                                        xcord = xstart1
                                        ycord = ix1
                                        cords = (xcord, ycord)
                                        numval = numval * int(num)
                                        numsym = 1
                                        values = (numval, numsym)
                                        if cords in syms:
                                            numsym = syms[cords][1]
                                            numval = numval * syms[cords][0]
                                            numsym += 1
                                            values = (numval, numsym)
                                            syms[cords] = values
                                        else:
                                            syms[cords] = values
        y += 1
        for cords in syms:
            if syms[cords][1] == 2:
                sums += syms[cords][0]
    return sums


if __name__ == "__main__":
    with open("input.txt", "r") as file:
        input_data = file.read()

    part_one_solution = solve_part_one(input_data)
    print(f"Part One Solution: {part_one_solution}")

    part_two_solution = solve_part_two(input_data)
    print(f"Part Two Solution: {part_two_solution}")
