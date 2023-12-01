import sys

template = """from aoc_prepare import PrepareAoc


def part1(inp):
    pass


def part2(inp):
    pass


def test_1_1():
    pass


def test_1_2():
    pass


def main(inp):
    print("Part1:", part1(inp.strip()))
    print("Part2:", part2(inp.strip()))


if __name__ == "__main__":
    prep = PrepareAoc({}, {})
    main(prep.get_content())"""

def main(year):
    for day in range(1, 26):
        file_name = f"d{year}_{day:02d}.py"
        print(f"Writing file '{file_name}'")
        with open(file_name, mode="wt", encoding="utf8") as out_file:
            out_file.write(template.format(year, day))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python d_templaty.py <year>")
    else:
        print("Creating files for year", sys.argv[1])
        main(int(sys.argv[1]))
