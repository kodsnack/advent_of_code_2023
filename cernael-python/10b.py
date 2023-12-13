def solve(lines):
    grid = {}
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            grid[(i,j)] = lines[i][j]
            if lines[i][j] == 'S':
                visits = [[(i,j)]]
    done = False
    while not done:
        poss = []
        for (i,j) in visits[-1]:
            curr = grid.pop((i,j), None)
            if curr == 'S':
                if grid.get((i+1,j)) and grid[(i+1,j)] in 'LJ|':
                    poss.append((i+1,j))
                if grid.get((i-1,j)) and grid[(i-1,j)] in 'F7|':
                    poss.append((i-1,j))
                if grid.get((i,j-1)) and grid[(i,j-1)] in 'LF-':
                    poss.append((i,j-1))
                if grid.get((i,j+1)) and grid[(i,j+1)] in 'J7-':
                    poss.append((i,j+1))
            if curr == 'L':
                if grid.get((i-1,j)) and grid[(i-1,j)] in 'F7|':
                    poss.append((i-1,j))
                if grid.get((i,j+1)) and grid[(i,j+1)] in 'J7-':
                    poss.append((i,j+1))
            if curr == 'J':
                if grid.get((i-1,j)) and grid[(i-1,j)] in 'F7|':
                    poss.append((i-1,j))
                if grid.get((i,j-1)) and grid[(i,j-1)] in 'LF-':
                    poss.append((i,j-1))
            if curr == '|':
                if grid.get((i+1,j)) and grid[(i+1,j)] in 'LJ|':
                    poss.append((i+1,j))
                if grid.get((i-1,j)) and grid[(i-1,j)] in 'F7|':
                    poss.append((i-1,j))
            if curr == 'F':
                if grid.get((i+1,j)) and grid[(i+1,j)] in 'LJ|':
                    poss.append((i+1,j))
                if grid.get((i,j+1)) and grid[(i,j+1)] in 'J7-':
                    poss.append((i,j+1))
            if curr == '7':
                if grid.get((i+1,j)) and grid[(i+1,j)] in 'LJ|':
                    poss.append((i+1,j))
                if grid.get((i,j-1)) and grid[(i,j-1)] in 'LF-':
                    poss.append((i,j-1))
            if curr == '-':
                if grid.get((i,j-1)) and grid[(i,j-1)] in 'LF-':
                    poss.append((i,j-1))
                if grid.get((i,j+1)) and grid[(i,j+1)] in 'J7-':
                    poss.append((i,j+1))
        if poss:
            visits.append(poss)
            
        else:
            done = True

    # out: -2 is wholly outside
    #       2 is wholly inside
    #      -1 is on path, inside downwards
    #       1 is on path, inside upwards
    out = -2
    nest = 0
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if (i,j) not in grid:
                p = lines[i][j]
                if out == -2:
                    if p == 'F':
                        out = -1
                    elif p == 'L':
                        out = 1
                    elif p == '|':
                        out = 2
                elif out == 2:
                    if p == 'F':
                        out = 1
                    elif p == 'L':
                        out = -1
                    elif p == '|':
                        out = -2

                elif out == -1:
                    if p == '7':
                        out = -2
                    elif p == 'J':
                        out = 2
                elif out == 1:
                    if p == '7':
                        out = 2
                    elif p == 'J':
                        out = -2

            elif out == 2:
                nest += 1
        
    return nest
if __name__ == '__main__':
    lines = []
    with open('10.txt') as f:
        for line in f.readlines():
            lines.append(line.strip())
    print(solve(lines))
