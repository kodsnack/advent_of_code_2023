from dataclasses import dataclass
from heapq import heappop, heappush


@dataclass
class SearchResult:
    path: list[object]
    cost: int
    end_state: object
    path_length: int


def unroll(node, previous):
    path = []

    while node in previous:
        path.append(node)
        node = previous[node]

    return path[::-1]


def sssp(graph, start, goal_function, step_finder):
    previous = {}
    frontier = [(0, start, None)]

    while True:
        steps, position, prev = heappop(frontier)

        if position in previous:
            continue

        previous[position] = prev

        if goal_function(position):
            path = unroll(position, previous)
            return SearchResult(path, steps, position, len(path))

        for cost, next_step in step_finder(graph, position):
            if next_step in previous:
                continue

            heappush(frontier, (steps+cost, next_step, position))


def custsort(l, comparator):
    n = len(l)

    if n < 2:
        return l

    a = l[:n//2]
    b = l[n//2:]

    ll = []

    la = len(a)
    lb = len(b)
    pa = 0
    pb = 0
    sa = custsort(a, comparator)
    sb = custsort(b, comparator)

    while pa < la and pb < lb:
        comp = comparator(sa[pa], sb[pb])

        if comp > 0:
            ll.append(sb[pb])
            pb += 1
        else:
            ll.append(sa[pa])
            pa += 1

    while pa < la:
        ll.append(sa[pa])
        pa += 1
    while pb < lb:
        ll.append(sb[pb])
        pb += 1

    return ll


def a_star(graph, start, goal, step_finder, heuristic):
    previous = {}
    frontier = [(heuristic(graph, start, goal), 0, start, None)]

    while True:
        best_possible, steps, state, prev = heappop(frontier)

        if state in previous:
            continue

        previous[state] = prev

        if best_possible == steps:
            path = unroll(state, previous)
            return SearchResult(path, steps, state, len(path))
        
        for next_state in step_finder(graph, state):
            if next_state in previous:
                continue

            h = heuristic(graph, next_state, goal)

            heappush(frontier, (h + steps + 1, steps + 1, next_state, state))