def solve(lines):
    points = [1 for _ in lines]
    for line in range(len(lines)):
        _, (win, have) = [
            [
                {
                    z for z in y.split()
                }
                for y in x.split('|')
            ]
            for x in lines[line].split(':')
        ]
        
        for i in range(len(win.intersection(have))):
            points[line+i+1] += points[line]

    return sum(points)
if __name__ == '__main__':
    lines = []
    with open('4.txt') as f:
        for line in f.readlines():
            lines.append(line)
    print(solve(lines))
