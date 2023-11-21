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