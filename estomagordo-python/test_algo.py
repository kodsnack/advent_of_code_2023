from algo import a_star, custsort, merge_ranges, sssp


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

    assert 52 == shortest_path.cost
    assert 100 == shortest_path.end_state
    assert [0, 2, 100] == shortest_path.path


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

    assert 52 == shortest_path.cost
    assert (1, 1, 1) == shortest_path.end_state
    assert [(0, 0, 0), (1, 0, 1), (1, 1, 1)] == shortest_path.path


def test_custsort():
    l = [5, 2, 1, 0, 9]

    resreg = custsort(l, lambda a,b: -1 if a < b else 1)
    resrev = custsort(l, lambda a,b: -1 if a >= b else 1)

    assert [0, 1, 2, 5, 9] == resreg
    assert [9, 5, 2, 1, 0] == resrev


def test_a_star():
    graph = {
        'abc': ['bac', 'acb'],
        'acb': ['cab', 'abc'],
        'bac': ['abc', 'bca'],
        'bca': ['cba', 'bac'],
        'cab': ['acb', 'cba'],
        'cba': ['bca', 'cab'],
    }

    start = 'cba'
    goal = 'abc'

    optimal = 3

    def step_finder(graph, state):
        return graph[state]
    
    def heuristic(graph, state, goal):
        def distance_for(element):
            return abs(state.index(element) - goal.index(element))
        
        return (sum(distance_for(element) for element in state) + 1) // 2
    
    result = a_star(graph, start, goal, step_finder, heuristic)

    assert optimal == result.cost
    assert 'abc' == result.end_state
    assert 4 == result.path_length


def test_merge_ranges():
    a = [-4, 10]
    b = [7, 15]
    c = [8, 9]
    d = [14, 14]
    e = [19, 29]
    f = [34, 40]
    g = [31, 34]
    h = [50, 60]
    i = [45, 55]
    j = [68, 80]
    k = [78, 84]

    ranges = [a, b, c, d, e, f, g, h, i, j, k]

    expected = [[-4, 15], [19, 29], [31, 40], [45, 60], [68, 84]]

    assert expected == merge_ranges(ranges)