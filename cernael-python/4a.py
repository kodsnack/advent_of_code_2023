def solve(lines):
    points = 0
    for line in lines:
        _, (win, have) = [[{z for z in y.split()} for y in x.split('|')] for x in line.split(':')]
        points += int(2**(len(win.intersection(have))-1))

    return points
if __name__ == '__main__':
    lines = []
    with open('4.txt') as f:
        for line in f.readlines():
            lines.append(line)
    print(solve(lines))
