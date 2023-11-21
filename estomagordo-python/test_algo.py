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

    assert 52 == shortest_path


def test_sssp_three_dimensional():
    def goal_function_is_100(position):
        return position == (1, 1, 1)

    def step_finder(graph, position):
        return graph[position]

    graph = {
        (0, 0, 0): ((1, (0, 1, 0)), (2, (1, 0, 1))),
        (0, 1, 0): ((100, (1, 1, 1)),),
        (1, 0, 1): ((50, (1, 1, 1)),),
    }

    start = (0, 0, 0)

    shortest_path = sssp(graph, start, goal_function_is_100, step_finder)

    assert 52 == shortest_path