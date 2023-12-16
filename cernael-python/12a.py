def solve(lines):
    res = 0
    for line in lines:
        m, d = line.split()
        d = [int(i) for i in d.split(',')]
        if works(m,d): res += 1
    return res

def works(m,d):
    return [len(s) for s in m.split('.') if s] == d

if __name__ == '__main__':
    lines = []
    with open('12t.txt') as f:
        for line in f.readlines():
            lines.append(line.strip())
    print(solve(lines))
