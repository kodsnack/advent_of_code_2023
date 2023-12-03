def solve(lines):
    res = 0
    for l in lines:
        title, game = l.split(': ')
        n = title.split()[1]
        rounds = [{k:int(v) for (v, k) in map(lambda x: x.split(), r.split(', '))} for r in game.split('; ')]
        
        red = max(map(lambda x: x.get('red',0),rounds))
        green = max(map(lambda x: x.get('green',0),rounds))
        blue = max(map(lambda x: x.get('blue',0),rounds))
        res += red*green*blue
    return res




if __name__ == '__main__':
    lines = []
    with open('2.txt') as f:
        for line in f.readlines():
            lines.append(line)
    print(solve(lines))
