def solve(lines):
    l = lines.pop(0).split(':')[1].split()
    seeds = {int(n) for n in l}

    addseeds, removeseeds = set(), set()
    for l in lines:
        if not l.strip(): continue
        if l.find(':') >= 0:
            seeds = addseeds | (seeds - removeseeds)
            addseeds, removeseeds = set(), set()
            continue
        (dest, src, n) = map(int, l.split())
        for s in seeds:
            if src <= s < src+n:
                removeseeds.add(s)
                addseeds.add(s+dest-src)
    seeds = addseeds | (seeds - removeseeds)
    return min(seeds)

if __name__ == '__main__':
    lines = []
    with open('5.txt') as f:
        for line in f.readlines():
            lines.append(line)
    print(solve(lines))
