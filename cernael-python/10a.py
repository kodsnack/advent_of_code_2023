def solve(lines):
    grid = {}
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] != '.':
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


        
    return len(visits) - 1
if __name__ == '__main__':
    lines = []
    with open('10.txt') as f:
        for line in f.readlines():
            lines.append(line.strip())
    print(solve(lines))
