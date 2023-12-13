from functools import reduce
def solve(lines):
    res = 0
    for l in lines:
        l = [[int(n) for n in l.split()]]
        cont = True
        while cont:
            cont = False
            ny = []
            for n in range(len(l[-1]) - 1):
                diff = l[-1][n+1] - l[-1][n]
                ny.append(diff)
                if diff != 0:
                    cont = True
            l.append(ny)
        res += reduce(lambda acc,x: x[0]-acc, reversed(l), 0)
    return res

if __name__ == '__main__':
    lines = []
    with open('9.txt') as f:
        for line in f.readlines():
            lines.append(line.strip())
    print(solve(lines))
