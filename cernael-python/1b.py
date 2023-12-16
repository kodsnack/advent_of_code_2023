def solve(lines):
    return sum(
        map(extraxt_nums, lines)
    )

def extraxt_nums(l):
    ns = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    tens, ones = 0,0
    for c in range(len(l)):
        if tens: break
        if l[c].isdigit():
            tens = int(l[c])
        for n in range(len(ns)):
            if l[c:].find(ns[n]) == 0:
                tens = (n+1)
    for c in reversed(range(len(l))):
        if ones: break
        if l[c].isdigit():
            ones = int(l[c])
        for n in range(len(ns)):
            if l[c:].find(ns[n]) == 0:
                ones = (n+1)
  
    return tens*10 + ones

if __name__ == '__main__':
    lines = []
    with open('1.txt') as f:
        for line in f.readlines():
            lines.append(line)
    print(solve(lines))
