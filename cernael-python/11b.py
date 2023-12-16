def solve(lines):
    dubrow, dubcol = [],[]
    for i in range(len(lines)):
        if lines[i].find('#') == -1:
            dubrow.append(i)
    for j in range(len(lines[0])):
        l = ''.join([c[j] for c in lines])
        if l.find('#') == -1:
            dubcol.append(j)
    stars = []
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] == '#':
                stars.append((i,j))
    res = 0
    for i in range(1,len(stars)):
        for j in range(i):

            s1, s2 = stars[i], stars[j]
            mh = abs(s1[0] - s2[0]) + abs(s1[1] - s2[1])
            res += mh
            for x in dubrow:
                if s1[0] < x < s2[0] or s1[0] > x > s2[0]:
                    res += 1000000-1
            for x in dubcol:
                if s1[1] < x < s2[1] or s1[1] > x > s2[1]:
                    res += 1000000-1
    return res

if __name__ == '__main__':
    lines = []
    with open('11.txt') as f:
        for line in f.readlines():
            lines.append(line.strip())
    print(solve(lines))
