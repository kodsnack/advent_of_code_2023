#!/usr/bin/env python3

from aoclib import *

import re

def find(st, col):
    rm = re.search(f'.*?([0-9]+) {col}.*?', st)
    if rm:
        return int(rm.group(1))
    else:
        return 0

def main():
    data = readdata()
    ans1 = 0
    ans2 = 0
    for l in data:
        l = l.strip()
        i = l.split(':')
        games = re.search('Game ([0-9]+)', i[0])
        game = int(games.group(1))
        k = i[1].split(';')
        (mr, mg, mb) = (0,0,0)
        bad = False
        for s in k:
            r = find(s, 'red')
            g = find(s, 'green')
            b = find(s, 'blue')
            mr = max(r, mr)
            mg = max(g, mg)
            mb = max(b, mb)
        if mr <= 12 and mg <= 13 and mb <= 14:
            ans1 += game
        ans2 += mr*mg*mb
    return ans1,ans2

if __name__ == '__main__':
    checkans(*main())
