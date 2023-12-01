from aoc_prepare import PrepareAoc


def decode_line(line, d):
    digits = []
    i = 0
    while i < len(line):
        for word in d:
            if line[i:].startswith(word):
                digits.append(d[word])
                break
        i += 1
    return (10*int(digits[0]) + int(digits[-1]))


def decode_file(inp, d):
    return sum((decode_line(line, d) for line in inp.splitlines()))

def part1(inp):
    d = {"0":0, "1":1, "2": 2, "3":3, "4": 4, "5":5, "6":6, "7":7, "8":8, "9":9}
    return decode_file(inp, d)


def part2(inp):
    d = {"one":1, "two":2, "three":3, "four":4, "five":5, "six":6, "seven":7, "eight":8, "nine":9,
        "0":0, "1":1, "2": 2, "3":3, "4": 4, "5":5, "6":6, "7":7, "8":8, "9":9}
    return decode_file(inp, d)


def test_1_1():
    assert 142 == part2("""1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet""")


def test_2_2():
    assert 281 == part2("""two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen""")


def main(inp):
    print("Part1:", part1(inp.strip()))
    print("Part2:", part2(inp.strip()))


if __name__ == "__main__":
    prep = PrepareAoc(2023, 1)
    main(prep.get_content())
