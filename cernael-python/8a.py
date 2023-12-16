class Node:
    def __init__(self, name):
        self.name = name
        self.left = None
        self.right = None
    def left(self, left):
        self.left = left
    def right(self, right):
        self.right = right
    def __repr__(self):
        return f"{self.name}: ({self.left.name}, {self.right.name})"


def solve(lines):
    instr = lines.pop(0)
    n = 0
    terr = {}
    for line in lines:
        if line:
            name, lr = [s.strip('( )') for s in line.split('=')]
            left, right = lr.split(', ')
            for node in [name, left, right]:
                if node not in terr:
                    terr[node] = Node(node)
            if not terr[name].left:
                terr[name].left = terr[left]
            if not terr[name].right:
                terr[name].right = terr[right]



    curr = terr['AAA']
    while True:
        d = instr[n % len(instr)]
        n += 1
        curr = curr.left if d == 'L' else curr.right
        if curr.name == 'ZZZ':
            break
    return n

if __name__ == '__main__':
    lines = []
    with open('8.txt') as f:
        for line in f.readlines():
            lines.append(line.strip())
    print(solve(lines))
