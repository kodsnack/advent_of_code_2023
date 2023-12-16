def solve(lines):
    p = [int(''.join([c for c in l.split(':')[1] if c.isdigit()])) for l in lines]

    p = [p]
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
