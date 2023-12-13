def solve(lines):
    res = 0
    for l in lines:
        title, game = l.split(': ')
        n = title.split()[1]
        if [int(n) for n in game.split() if n[0].isdigit() and int(n) > 14]:
            continue
        if (game.find('14 green') != -1
         or game.find('14 red')   != -1
         or game.find('13 red')   != -1):
            continue
        res += int(n)
    return res




if __name__ == '__main__':
    lines = []
    with open('2.txt') as f:
        for line in f.readlines():
            lines.append(line)
    print(solve(lines))
