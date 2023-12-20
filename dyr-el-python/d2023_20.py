from aoc_prepare import PrepareAoc

from position import Pos2D
from collections import namedtuple, deque, Counter
from prio_queue import PrioQueue


def parse(inp):
    d = dict()
    inputs = dict()
    for line in inp.splitlines():
        items = line.split(' ')
        if items[0][0] in '%&':
            tp, name, dests = items[0][0], items[0][1:], items[2:]
            dests = [dest[:-1] if dest[-1]==',' else dest for dest in dests]
            d[name] = (tp, dests)
            for dest in dests:
                if dest not in inputs:
                    inputs[dest] = list()
                inputs[dest].append(name)
        else:
            tp, name, dests = "broadcast", "broadcast", items[2:]
            dests = [dest[:-1] if dest[-1]==',' else dest for dest in dests]
            d[name] = (tp, dests)
            for dest in dests:
                if dest not in inputs:
                    inputs[dest] = list()
                inputs[dest].append(name)
    return d, inputs


def part1(inp):
    d, inputs = parse(inp)
    conj = {name:{input:"low" for input in inputs[name]} for name in d if d[name][0] == "&"}
    state = {name:"low" for name in d}
    count = {"low": 0, "high": 0}
    for i in range(1000):
        q = deque([["broadcast", "low", "button"]])
        while q:
            receiver, signal, sender = q.popleft()
            count[signal] += 1
            if receiver == "rx":
                d[receiver] = "rx", "rx"
            tp, dests = d[receiver]
            if receiver == "broadcast":
                for dest in dests:
                    q.append((dest, signal, "broadcast"))
            elif tp == "%":
                if signal == "low":
                    state[receiver] = {"low": "high", "high": "low"}[state[receiver]]
                    for dest in dests:
                        q.append((dest, state[receiver], receiver))
            elif tp == "&":
                conj[receiver][sender] = signal
                if all((x == "high" for x in conj[receiver].values())):
                    for dest in dests:
                        q.append((dest, "low", receiver))
                else:
                    for dest in dests:
                        q.append((dest, "high", receiver))
    return count["low"] * count["high"]

def part2(inp):
    d, inputs = parse(inp)
    conj = {name:{input:"low" for input in inputs[name]} for name in d if d[name][0] == "&"}
    state = {name:"low" for name in d}
    count = {"low": 0, "high": 0}
    rx = None
    button = 0
    while True:
        oldState = dict(conj)
        button += 1
        q = deque([["broadcast", "low", "button"]])
        while q:
            receiver, signal, sender = q.popleft()
            count[signal] += 1
            if receiver == "rx":
                rx = signal
                continue
            tp, dests = d[receiver]
            if receiver == "broadcast":
                for dest in dests:
                    q.append((dest, signal, "broadcast"))
            elif tp == "%":
                if signal == "low":
                    state[receiver] = {"low": "high", "high": "low"}[state[receiver]]
                    for dest in dests:
                        q.append((dest, state[receiver], receiver))
            elif tp == "&":
                conj[receiver][sender] = signal
                if all((x == "high" for x in conj[receiver].values())):
                    for dest in dests:
                        q.append((dest, "low", receiver))
                else:
                    for dest in dests:
                        q.append((dest, "high", receiver))
        if rx == "low":
            return button
        print(conj)
        input()


def test_1_1():
    assert 32000000 == part1("""broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a""")

def test_1_2():
    assert 11687500 == part1("""broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output""")


def test_1_2():
    pass


def main(inp):
    print("Part1:", part1(inp.strip()))
    print("Part2:", part2(inp.strip()))


if __name__ == "__main__":
    prep = PrepareAoc(2023, 20)
    main(prep.get_content())