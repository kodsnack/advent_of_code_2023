def solve(lines):
    return sum(
        map(extraxt_nums, lines)
    )

def extraxt_nums(l):
    n = [c for c in l if c.isdigit()]
    return int(n[0]+n[-1])

if __name__ == '__main__':
    lines = []
    with open('1.txt') as f:
        for line in f.readlines():
            lines.append(line)
    print(solve(lines))
