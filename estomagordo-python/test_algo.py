from algo import sssp


def test_sssp_greediness():
    def goal_function_is_100(position):
        return position == 100
    
    def step_finder(graph, position):
        return graph[position]
    
    graph = {
        0: ((1, 1), (2, 2)),
        1: ((100, 100),),
        2: ((50, 100),),
    }

    start = 0

    shortest_path = sssp(graph, start, goal_function_is_100, step_finder)

    assert(52 == shortest_path)