from aoc_prepare import PrepareAoc

from position import Pos2D
from collections import namedtuple, deque, Counter
from prio_queue import PrioQueue


def parse(inp):
    inp1, inp2 = inp.split('\n\n')
    result = dict()
    for lidx, line in enumerate(inp1.splitlines()):
        workflow, _,  rules = line.partition('{')
        rules = rules[:-1]
        rules = rules.split(',')
        rules2 = list()
        for rule in rules:
            if rule.count(':'):
                r, _, d = rule.partition(':')
                if r.count('>'):
                    v, _, a = r.partition('>')
                    rules2.append((d, (v , '>', int(a))))
                if r.count('<'):
                    v, _, a = r.partition('<')
                    rules2.append((d, (v , '<', int(a))))
            else:
                rules2.append((rule,None))
        result[workflow] = rules2
    result3 = list()
    for lidx, line in enumerate(inp2.splitlines()):
        values = line[1:-1].split(',')
        d = dict()
        for value in values:
            letter, _, v = value.partition('=')
            v = int(v)
            d[letter] = v
        result3.append(d)
    return result, result3

def process_package(package, workflows):
    print('->', package)
    workflow = 'in'
    while workflow not in ('R', 'A'):
        print(workflow)
        wf = workflows[workflow]
        print(" ", wf)
        for rule in wf:
            print(" ", rule)
            if rule[1] is None:
                workflow = rule[0]
                print("Default", rule[0])
                break
            elif rule[1][1] == '>':
                print(package[rule[1][0]], ">", rule[1][2])
                if package[rule[1][0]] > rule[1][2]:
                    print(rule[0])
                    workflow = rule[0]
                    break
            elif rule[1][1] == '<':
                print(package[rule[1][0]], "<", rule[1][2])
                if package[rule[1][0]] < rule[1][2]:
                    print(rule[1])
                    workflow = rule[0]
                    break
            else:
                print("Error in package worflow", package, rule)
    return workflow == 'A'
        


def part1(inp):
    workflows, packages = parse(inp)
    sm = 0
    for package in packages:
        if process_package(package, workflows):
            sm += sum(package.values())
    return sm


def calc_backwards(workflows):
    conditions = {'A': {'x':(1, 4000), 'm':(1 4000), 'a': (1, 4000), 's': (1, 4000)}}
    for workflow in workflows:
        for rule in workflow:
            destination, cond = rule
            if destination not in conditions:
                continue
            



def part2(inp):
    pass

def test_1_1():
    assert(19114 == part1("""px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""))


def test_1_2():
    assert(0 == part2("""inp"""))


def main(inp):
    print("Part1:", part1(inp.strip()))
    print("Part2:", part2(inp.strip()))


if __name__ == "__main__":
    prep = PrepareAoc(2023, 19)
    main(prep.get_content())