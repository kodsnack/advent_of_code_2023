def solve(lines):
    p = [[int(n) for n in l.split()[1:]] for l in lines]
    p = zip(p[0],p[1])
    res = 1

    for x in p:
        n = 0
        while n*(x[0]-n) <= x[1]:
            #print(n*(x[0]-n),x,n)
            n += 1
        s = (x[0]+1)-(n)*2
       # print(n*(x[0]-n),x, res, s, res*s,x,n)
        res *= s

    return res

if __name__ == '__main__':
    lines = []
    with open('6.txt') as f:
        for line in f.readlines():
            lines.append(line.strip())
    print(solve(lines))
