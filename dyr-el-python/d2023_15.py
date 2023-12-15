from aoc_prepare import PrepareAoc

def parse(inp):
    result = list()
    return inp.split(',')


def hash(s):
    result = 0
    for c in s:
        result += ord(c)
        result = (result * 17 ) % 256
    return result


def part1(inp):
    return sum((hash(s) for s in parse(inp)))


def dash(box, label, _):
    for bidx, pos in enumerate(box):
        if pos[0] == label:
            del box[bidx]
            return


def equals(box, label, focal):
    for bidx, pos in enumerate(box):
        if pos[0] == label:
            box[bidx] = (label, focal)
            return
    box.append((label, focal))


def parse2(inp):
    for s in inp.split(','):
        if s.count('-') > 0:
            yield s[:-1], dash, hash(s[:-1]), 0
        else:
            label, n = s.split('=')
            yield label, equals, hash(label), int(n)


def focus_power(boxes):
    return sum(((bidx * sidx * slot[1])
                 for bidx, box in enumerate(boxes, start=1)
                 for sidx, slot in enumerate(box, start=1)))


def part2(inp):
    boxes = [list() for _ in range(256)]
    for label, op, n, focal in parse2(inp):
        op(boxes[n], label, focal)
    return focus_power(boxes)


def test_1_0():
    assert 52 == hash("""HASH""")


def test_1_1():
    assert 1320 == part1("""rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7""")


def test_1_2():
    assert 145 == part2("""rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7""")

def main(inp):
    print("Part1:", part1(inp.strip()))
    print("Part2:", part2(inp.strip()))

from timeit import Timer
def main_timer(inp):
    timer = Timer(stmt='part1(inp.strip())', setup=f"inp='''{inp}'''", globals=globals())
    iterations, time = timer.autorange()
    print("average time for part 1 =", time/iterations)
    timer = Timer(stmt='part2(inp.strip())', setup=f"inp='''{inp}'''", globals=globals())
    iterations, time = timer.autorange()
    print("average time for part 2 =", time/iterations)

if __name__ == "__main__":
    prep = PrepareAoc(2023, 15)
    main(prep.get_content())
    main_timer(prep.get_content())