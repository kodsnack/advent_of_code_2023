from aoc_prepare import PrepareAoc
from position import Pos2D
from collections import namedtuple, deque, Counter
from prio_queue import PrioQueue

def parse(inp):
    result = dict()
    for lidx, line in enumerate(inp.splitlines()):
        for cidx, c in enumerate(line):
            result[Pos2D(cidx, lidx)] = int(c)
    return result, Pos2D(max((p.x for p in result)), max((p.y for p in result)))


def traverse(mp, max_pos):
    State = namedtuple('State', ['cost', 'position', 'direction', 'steps'])
    state = State(cost=0, position=Pos2D(0, 0), direction=Pos2D(1, 0), steps=0)
    visited = set()
    queue = PrioQueue([state], comparison_key=lambda x:(x.cost, x.position.manhattan(max_pos)))
    while queue:
        current = queue.pop()
        if (current.position, current.direction, current.steps) in visited:
            continue
        visited.add((current.position, current.direction, current.steps))
        if current.position == max_pos:
            return current.cost
        if current.steps < 3:
            new_position = current.position + current.direction
            if new_position in mp:
                new_state = State(cost=(current.cost + mp[new_position]),
                                  position=new_position,
                                  direction=current.direction,
                                  steps=(current.steps + 1)
                                  )
                queue.push(new_state)
        new_direction = current.direction.left()
        new_position = current.position + new_direction
        if new_position in mp:
            new_state = State(cost=(current.cost + mp[new_position]),
                              position=new_position,
                              direction=new_direction,
                              steps=1)
            queue.push(new_state)
        new_direction = current.direction.right()
        new_position = current.position + new_direction
        if new_position in mp:
            new_state = State(cost=(current.cost + mp[new_position]),
                              position=new_position,
                              direction=new_direction,
                              steps=1)
            queue.push(new_state)
    return None


def traverse2(mp, max_pos):
    State = namedtuple('State', ['cost', 'position', 'direction', 'steps'])
    state = State(cost=0, position=Pos2D(0, 0), direction=Pos2D(1, 0), steps=0)
    visited = set()
    queue = PrioQueue([state], comparison_key=lambda x:(x.cost, x.position.manhattan(max_pos)))
    while queue:
        current = queue.pop()
        if (current.position, current.direction, current.steps) in visited:
            continue
        visited.add((current.position, current.direction, current.steps))
        if current.position == max_pos and current.steps > 3:
            return current.cost
        if current.steps < 10:
            new_position = current.position + current.direction
            if new_position in mp:
                new_state = State(cost=(current.cost + mp[new_position]),
                                  position=new_position,
                                  direction=current.direction,
                                  steps=(current.steps + 1)
                                  )
                queue.push(new_state)
        if current.steps > 3:
            new_direction = current.direction.left()
            new_position = current.position + new_direction
            if new_position in mp:
                new_state = State(cost=(current.cost + mp[new_position]),
                                  position=new_position,
                                  direction=new_direction,
                                  steps=1)
                queue.push(new_state)
            new_direction = current.direction.right()
            new_position = current.position + new_direction
            if new_position in mp:
                new_state = State(cost=(current.cost + mp[new_position]),
                                  position=new_position,
                                  direction=new_direction,
                                  steps=1)
                queue.push(new_state)
    return None


def part1(inp):
    result, max_pos = parse(inp)
    return traverse(result, max_pos)


def part2(inp):
    result, max_pos = parse(inp)
    return traverse2(result, max_pos)


example1 = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""
def test_1_1():
    assert 102 == part1(example1)


example2 = example1
#example2 = """"""
def test_1_2():
    assert 94 == part2(example2)


def main(inp):
    print("Part1:", part1(inp.strip()))
    print("Part2:", part2(inp.strip()))


if __name__ == "__main__":
    prep = PrepareAoc(2023, 17)
    main(prep.get_content())