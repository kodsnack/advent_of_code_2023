def solve(lines):
    res = 0
    for i in range(len(lines)):
        n,start,end = "",0,0
        l = lines[i]
        for j in range(len(l)):
            if l[j].isdigit():
                n += l[j]
                end = j+1
            else:
                s = max(start-1,0)
                e = min(end+1,len(l)-1)
                t = max(i-1, 0)
                b = min(i+1, len(lines)-1)
                if (n and 
                    ((s != start and l[s] != '.') or
                     (e != end and l[end] != '.') or
                     (t!=i and lines[t][s:e] != '.'*(e-s)) or
                     (b!=i and lines[b][s:e] != '.'*(e-s)))):
                    res += int(n)

                n,start = "", j+1
    return res

if __name__ == '__main__':
    lines = []
    with open('3.txt') as f:
        for line in f.readlines():
            lines.append(line)
    print(solve(lines))
