import re

from fractions import Fraction
from functools import reduce
from itertools import product


def diffs(a, b):
    return (p[0] - p[1] for p in zip(a, b))


def distance_sq(a, b):
    return sum(d**2 for d in diffs(a, b))


def distance(a, b):
    return distance_sq(a, b)**0.5


def ints(line):
    pattern = re.compile(r'-?\d+')

    return [int(val) for val in re.findall(pattern, line) if val]


def manhattan(a, b):
    return sum(abs(d) for d in diffs(a, b))


def neighs(y, x):
    return ((y-1,x), (y+1,x), (y,x-1), (y,x+1))


def neighs_bounded(y, x, rmin, rmax, cmin, cmax):
    return tuple([n for n in neighs(y, x) if rmin <= n[0] <= rmax and cmin <= n[1] <= cmax])


def eight_neighs(y, x):
    return tuple([(y+dy, x+dx) for dy in range(-1, 2) for dx in range(-1, 2) if dy != 0 or dx != 0])


def eight_neighs_bounded(y, x, rmin, rmax, cmin, cmax):
    return tuple([n for n in eight_neighs(y, x) if rmin <= n[0] <= rmax and cmin <= n[1] <= cmax])


def grouped_lines(lines):
    groups = []
    group = []

    for line in lines:
        if not line.strip():
            groups.append(group)
            group = []
        else:
            group.append(line.rstrip())

    if group:
        groups.append(group)

    return groups


def n_neighs(point):
    n = len(point)

    for delta in product(range(-1, 2), repeat=n):
        if any(val != 0 for val in delta):
            yield tuple((point[i] + delta[i] for i in range(n)))


def multall(nums):
    return reduce(lambda a,b: a*b, nums)


def hexneighs(r, c):
    neighs = { (r, c+1), (r, c-1), (r-1, c), (r+1, c) }

    if r % 2:
        neighs |= { (r+1, c-1), (r-1, c-1) }
    else:
        neighs |= { (r+1, c+1), (r-1, c+1) }

    return neighs


def columns(matrix):
    return [[line[x] for line in matrix] for x in range(len(matrix[0]))]


def digits(line):
    pattern = re.compile(r'\d?')

    return [int(val) for val in re.findall(pattern, line) if val]


def chunks(l, n):
    for x in range(0, len(l), n):
        yield l[x:x+n]


def chunks_with_overlap(l, n):
    for x in range(n, len(l)+1):
        yield l[x-n:x]


def positives(line):
    return list(map(abs, ints(line)))


def rays(grid, y, x):
    return [
     [grid[y][dx] for dx in range(x)],
     [grid[y][dx] for dx in range(x+1, len(grid[0]))],
     [grid[dy][x] for dy in range(y)],
     [grid[dy][x] for dy in range(y+1, len(grid))]
    ]


def rays_from_inside(grid, y, x):
    return [
     [grid[y][dx] for dx in range(x)][::-1],
     [grid[y][dx] for dx in range(x+1, len(grid[0]))],
     [grid[dy][x] for dy in range(y)][::-1],
     [grid[dy][x] for dy in range(y+1, len(grid))]
    ]


def adjacent(a, b):
    return manhattan(a, b) == 1


def words(line):
    pattern = re.compile(r'[a-zA-Z]+')

    return [word for word in re.findall(pattern, line)]


def between(point, a, b, strictly_different=True):
    if strictly_different:
        return a < point < b or b < point < a
    
    return a <= point <= b or b <= point <= a


def overlap(a, b):
    return between(a[0], *b, False) or between(a[1], *b, False) or between(b[0], *a, False) or between(b[1], *a, False)


def dimensions(grid):
    return len(grid), len(grid[0])


def sum_of_differences(l):
    return sum((l[i] - l[i-1]) * (len(l) - i) * i for i in range(1, len(l)))


def rim(matrix):
    h, w = dimensions(matrix)

    top = [(0, x, matrix[0][x]) for x in range(w)]
    bottom = [(h-1, x, matrix[h-1][x]) for x in range(w)]
    left = [(y, 0, matrix[y][0]) for y in range(1, h-1)]
    right = [(y, w-1, matrix[y][w-1]) for y in range(1, h-1)]

    return top + bottom + left + right


def junctions(matrix, closed=None, open=None):
    h, w = dimensions(matrix)

    def is_open(y, x):
        if open:    
            return matrix[y][x] in open
        
        return matrix[y][x] not in closed
    
    def open_neighbour_count(y, x):
        return sum(is_open(ny, nx) for ny, nx in neighs_bounded(y, x, 0, h-1, 0, w-1))
    
    out = []

    for y, x in product(range(h), range(w)):
        if is_open(y, x) and open_neighbour_count(y, x) > 2:
            out.append((y, x))

    return out


def solve_system(equations):
    h, w = dimensions(equations)
    used_pivots = set()
    equations = [[Fraction(val) for val in equation] for equation in equations]

    for pos in range(w-1):
        for i, equation in enumerate(equations):
            val = equation[pos]

            if i in used_pivots or val == Fraction(0):
                continue

            used_pivots.add(i)

            for j in range(w):
                equations[i][j] /= val

            for j in range(h):
                if j == i:
                    continue

                factor = -equations[j][pos]

                for k in range(w):
                    equations[j][k] += factor * equations[i][k]

            break

    if len(used_pivots) < w - 1:
        return False, [-1 for _ in range(w-1)]

    return True, [[equation for equation in equations if equation[j] == Fraction(1)][0][-1] for j in range(w-1)]