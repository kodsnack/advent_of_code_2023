from heapq import heappop, heappush


def sssp(graph, start, goal_function, step_finder):
    seen = set()
    frontier = [(0, start)]

    while True:
        steps, position = heappop(frontier)

        if position in seen:
            continue

        seen.add(position)

        if goal_function(position):
            return steps

        for cost, next_step in step_finder(graph, position):
            if next_step in seen:
                continue

            heappush(frontier, (steps+cost, next_step))


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


def a_star(graph, start, step_finder, heuristic):
    seen = set()
    frontier = [(heuristic(graph, start), 0, start)]

    while True:
        best_possible, steps, state = heappop(frontier)

        if state in seen:
            continue

        seen.add(state)

        if best_possible == steps:
            return state
        
        for next_state in step_finder(graph, state):
            if next_state in seen:
                continue

            h = heuristic(graph, next_state)

            heappush(frontier, (h + steps + 1, steps + 1, next_state))