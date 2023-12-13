class Hand:
    def __init__(self, hand, bid):
        self.hand = hand
        self.bid = int(bid)
        s = sorted(hand)
     #   print(s)
        if s[0] == s[1] == s[2] == s[3] == s[4]:
            self.type = 'five'
        elif s[1] == s[2] == s[3] and (s[2] == s[0] or s[2] == s[4]):
            self.type = 'four'
        elif s[0] == s[1] and s[3] == s[4] and (s[2] == s[0] or s[2] == s[4]):
            self.type = 'full'
        elif s[0] == s[1] == s[2] or s[1] == s[2] == s[3] or s[2] == s[3] == s[4]:
            self.type = 'threes'
        elif (s[0] == s[1] and s[2] == s[3]) or (s[0] == s[1] and s[3] == s[4]) or (s[1] == s[2] and s[3] == s[4]):
            self.type = 'twopair'
        elif s[0] == s[1] or s[1] == s[2] or s[2] == s[3] or s[3] == s[4]:
            self.type = 'twos'
        else:
            self.type = 'untyped'
    def __lt__(self, other):
        if self.type != other.type:
            return self.type < other.type
        for i in range(len(self.hand)):
            if self.hand[i] != other.hand[i]:
                return self.hand[i] < other.hand[i]
        return True

def solve(lines):
    hands = [Hand(l.split()[0], l.split()[1]) for l in lines]
    hands.sort()
    res = 0
    for i in range(len(hands)):
        res += hands[i].bid * (i+1)
    return res

if __name__ == '__main__':
    lines = []
    with open('7.txt') as f:
        for line in f.readlines():
            lines.append(line.strip())
    print(solve(lines))
