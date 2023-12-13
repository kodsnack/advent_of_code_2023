from functools import reduce
class Ranges:
    def __init__(self):
        self.ranges = []
        self.merge()
    
    def merge(self):
        if len(self.ranges) <= 1: return
        self.ranges.sort()
        def fun (acc, x):
            if acc[-1][1]+1 >= x[0]:
                y = acc.pop()
                acc.append((y[0], max(x[1], y[1])))
            else: acc.append(x)
            return acc
        self.ranges = reduce(fun, self.ranges[1:], self.ranges[:1])
            
    def append(self, start, end):
        # add a new range to the ranges set, merging with existing ranges as appropriate
        self.ranges.append((start,end))
        self.merge()

    def __repr__(self):
        return str(self.ranges)

    def remove(self, start, end):
        remainders, indices, removeds = [], [], []
        for r in self.ranges:
            s = start <= r[0] <= end
            e = start <= r[1] <= end
            # remove start
            if s and not e:
                indices.append(r)
                remainders.append((end+1, r[1]))
                removeds.append((r[0], end))
            # remove ALL
            elif s and e:
                indices.append(r)
                removeds.append((r[0], r[1]))
            # remove end
            elif not s and e:
                indices.append(r)
                remainders.append((r[0], start-1))
                removeds.append((start, r[1]))
            # remove MIDDLE
            elif start > r[0] and end < r[1]:
                indices.append(r)
                remainders.append((r[0], start-1))
                remainders.append((end+1, r[1]))
                removeds.append((start, end))
        for r in indices:
            self.ranges.remove(r)
        self.ranges += remainders
        self.ranges.sort()
        return removeds 


def solve(lines):
    l = lines.pop(0).split(':')[1].split()
    seeds = Ranges()
    while l:
        start = int(l.pop(0))
        seedcount = int(l.pop(0))
        seeds.append(start, start+seedcount-1)

    moves, removeds = [], []
    for l in lines:
        if not l.strip(): continue
        if l.find(':') >= 0:
            for r in moves:
                shift = r[0]-r[1]
                rem = seeds.remove(r[1], r[1] + r[2]-1)
                print('r',r, 'shift', shift, 'rem' , rem)
                removeds += [[y+shift for y in x] for x in rem]
            for r in removeds:
                seeds.append(r[0],r[1])
            moves, removeds = [], []
            continue
        (dest,src,num) = map(int, l.split())
        moves.append([dest,src,num])

    for r in moves:
        shift = r[0]-r[1]
        rem = seeds.remove(r[1], r[1] + r[2]-1)
        removeds += [[y+shift for y in x] for x in rem]
    for r in removeds:
        seeds.append(r[0],r[1])
    return seeds.ranges[0][0]

if __name__ == '__main__':
    lines = []
    with open('5.txt') as f:
        for line in f.readlines():
            lines.append(line)
    print("the result is:", solve(lines))
