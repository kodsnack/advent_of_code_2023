class Solver:
    def __init__(self, lines):
        self.gears = {}
        self.lines = lines

    def solve(self):
        for i in range(len(self.lines)):
            n,start,end = "",0,0
            l = self.lines[i]
            for j in range(len(l)):
                end = j+1
                if l[j].isdigit():
                    n += l[j]
                else:
                    s = max(start-1,0)
                    e = min(end,len(l)-1)
                    t = max(i-1, 0)
                    b = min(i+1, len(self.lines)-1)
                    if n:
                        self.find_gears(n, (i,s,e))
                        if t!=i:
                            self.find_gears(n, (t,s,e))
                        if b!=i:
                            self.find_gears(n, (b,s,e))

                    n,start = "", j+1
        return sum([v[0]*v[1] for v in self.gears.values() if len(v) == 2])

    def find_gears(self, n, ise):
        (i,s,e) = ise
        l = self.lines[i][s:e]
        x = [l.find('*')]
        if x[0] != -1:
            x2 = l.rfind('*')
            while x2 != x[0]:
                x.append(x2)
                x2 = l[:x[-1]].rfind('*')
            for g in x:
                prev = self.gears.get((i,g+s),[])
                if prev:
                    prev.append(int(n))
                else:
                    self.gears[(i,g+s)] = [int(n)]

if __name__ == '__main__':
    lines = []
    with open('3.txt') as f:
        for line in f.readlines():
            lines.append('.'+line.strip()+'.')
        line = '.'*len(lines[0])
        lines = [line]+lines+[line]
    x = Solver(lines)
    print(x.solve())
