#!/usr/bin/env python3

from aoclib import *

nums = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
}

def main():
    data = readdata()
    ans1 = 0
    ans2 = 0
    for l in data:
        l = l.strip()
        first = last = None
        for c in l:
            if c >= '0' and c <= '9':
                if not first:
                    first = c
                last = c
        if first and last:
            tmp = 10*int(first)+int(last)
        ans1 += tmp
    print(ans1)
    for l in data:
        l = l.strip()
        for idx in range(len(l)):
            for s,n in nums.items():
                if s == l[idx:idx+len(s)]:
                    l = l[:idx] + str(n) + l[idx+1:]
        first = last = None
        for c in l:
            if c >= '0' and c <= '9':
                if not first:
                    first = c
                last = c
        if first and last:
            tmp = 10*int(first)+int(last)
        ans2 += tmp
    return ans1, ans2

if __name__ == '__main__':
    checkans(*main())
