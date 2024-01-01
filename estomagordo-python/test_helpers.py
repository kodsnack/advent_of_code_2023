from fractions import Fraction

from helpers import distance, distance_sq, ints, manhattan, neighs, neighs_bounded, columns, digits, chunks, chunks_with_overlap, positives, rays, rays_from_inside, adjacent, eight_neighs, eight_neighs_bounded, hexneighs, n_neighs, overlap, words, between, dimensions, sum_of_differences, rim, junctions, solve_system


def test_distance():
    a = [2, 3]
    b = [5, 7]

    d = distance(a, b)
    expected = 5

    assert expected == d


def test_distance_flipped():
    b = [2, 3]
    a = [5, 7]

    d = distance(a, b)
    expected = 5

    assert expected == d


def test_distance_negatives():
    a = [-2, -3]
    b = [-5, -7]

    d = distance(a, b)
    expected = 5

    assert expected == d


def test_distance_3d():
    b = [2, -3, 9]
    a = [1, -5, 7]

    d = distance(a, b)
    expected = 3

    assert expected == d


def test_distance_sq_2d():
    a = [2, 3]
    b = [5, 7]

    d = distance_sq(a, b)
    expected = 25

    assert expected == d


def test_distance_sq_2d_flipped():
    b = [2, 3]
    a = [5, 7]

    d = distance_sq(a, b)
    expected = 25

    assert expected == d


def test_distance_sq_2d_negatives():
    a = [-2, -3]
    b = [-5, -7]

    d = distance_sq(a, b)
    expected = 25

    assert expected == d


def test_distance_sq_3d():
    b = [2, -3, 9]
    a = [1, -5, 7]

    d = distance_sq(a, b)
    expected = 9

    assert expected == d


def test_ints():
    s = 'What they-43 were 8 saying was <albeit 7> (9) mi85ninte and -2'

    nums = ints(s)
    expected = [-43, 8, 7, 9, 85, -2]

    assert expected == nums


def test_manhattan():
    a = [5, -4]
    b = [2, 3]

    d = manhattan(a, b)
    expected = 10

    assert expected == d


def test_manhattan_flipped():
    b = [5, -4]
    a = [2, 3]

    d = manhattan(a, b)
    expected = 10

    assert expected == d


def test_manhattan_same():
    a = [5, -4]
    b = [5, -4]

    d = manhattan(a, b)
    expected = 0

    assert expected == d


def test_manhattan_3d():
    a = [5, -4, 7]
    b = [2, 3, 11]

    d = manhattan(a, b)
    expected = 14

    assert expected == d


def test_neighs():
    y = 4
    x = 2

    neighbours = neighs(y, x)

    assert 4 == len(neighbours)
    assert (3, 2) in neighbours
    assert (5, 2) in neighbours
    assert (4, 1) in neighbours
    assert (4, 3) in neighbours


def test_neighs_negative():
    y = -4
    x = -2

    neighbours = neighs(y, x)

    assert 4 == len(neighbours)
    assert (-3, -2) in neighbours
    assert (-5, -2) in neighbours
    assert (-4, -1) in neighbours
    assert (-4, -3) in neighbours


def test_neighs_bounded_in_bounds():
    y = 5
    x = 6
    rmin = 0
    rmax = 10
    cmin = 0
    cmax = 10

    neighbours = neighs_bounded(y, x, rmin, rmax, cmin, cmax)

    assert 4 == len(neighbours)
    assert (4, 6) in neighbours
    assert (6, 6) in neighbours
    assert (5, 5) in neighbours
    assert (5, 7) in neighbours


def test_neighs_bounded_edge():
    y = 5
    x = 6
    rmin = 5
    rmax = 10
    cmin = 0
    cmax = 10

    neighbours = neighs_bounded(y, x, rmin, rmax, cmin, cmax)

    assert 3 == len(neighbours)
    assert (6, 6) in neighbours
    assert (5, 5) in neighbours
    assert (5, 7) in neighbours


def test_neighs_bounded_corner():
    y = 5
    x = 6
    rmin = 5
    rmax = 10
    cmin = 0
    cmax = 6

    neighbours = neighs_bounded(y, x, rmin, rmax, cmin, cmax)

    assert 2 == len(neighbours)
    assert (6, 6) in neighbours
    assert (5, 5) in neighbours


def test_columns():
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    cols = columns(matrix)

    assert [1, 4, 7] == cols[0]
    assert [2, 5, 8] == cols[1]
    assert [3, 6, 9] == cols[2]

    non_square_matrix = [[1, 2], [3, 4], [5, 6]]

    non_square_cols = columns(non_square_matrix)

    assert [1, 3, 5] == non_square_cols[0]
    assert [2, 4, 6] == non_square_cols[1]


def test_digits():
    s = '8936982'

    result = digits(s)

    assert [8,9,3,6,9,8,2] == result


def test_digits_with_other_characters():
    s = ' 8sg9!369;;82'

    result = digits(s)

    assert [8,9,3,6,9,8,2] == result


def test_chunks():
    l = [1, 2, 7, 10, 12, 2]

    twochunks = list(chunks(l, 2))
    threechunks = list(chunks(l, 3))

    assert [[1, 2], [7, 10], [12, 2]] == twochunks
    assert [[1, 2, 7], [10, 12, 2]] == threechunks


def test_chunks_with_overlap():
    l = [1, 2, 7, 10, 12, 2]

    twochunks = list(chunks_with_overlap(l, 2))
    threechunks = list(chunks_with_overlap(l, 3))

    assert [[1, 2], [2, 7], [7, 10], [10, 12], [12, 2]] == twochunks
    assert [[1, 2, 7], [2, 7, 10], [7, 10, 12], [10, 12, 2]] == threechunks


def test_positives():
    s = 'What they-43 were 8 saying was <albeit 7> (9) mi85ninte and -2'

    nums = positives(s)
    expected = [43, 8, 7, 9, 85, 2]

    assert expected == nums


def test_rays():
    grid = [
        [3, 0, 3, 7, 3],
        [2, 5, 5, 1, 2],
        [6, 5, 3, 3, 2],
        [3, 3, 5, 4, 9],
        [3, 5, 3, 9, 0]
    ]

    y = 2
    x = 2

    n = [3, 5]
    s = [5, 3]
    w = [6, 5]
    e = [3, 2]

    raysfrom = rays(grid, y, x)

    assert n in raysfrom
    assert s in raysfrom
    assert w in raysfrom
    assert e in raysfrom


def test_rays_from_inside():
    grid = [
        [3, 0, 3, 7, 3],
        [2, 5, 5, 1, 2],
        [6, 5, 3, 3, 2],
        [3, 3, 5, 4, 9],
        [3, 5, 3, 9, 0]
    ]

    y = 2
    x = 2

    n = [5, 3]
    s = [5, 3]
    w = [5, 6]
    e = [3, 2]

    raysfrom = rays_from_inside(grid, y, x)

    assert n in raysfrom
    assert s in raysfrom
    assert w in raysfrom
    assert e in raysfrom


def test_adjacent():
    one_d_a = [4]
    one_d_b = [5]
    one_d_c = [10]

    two_d_a = [4, 1]
    two_d_b = [3, 1]
    two_d_c = [4, 2]
    two_d_d = [3, 0]

    three_d_a = [1, 1, 1]
    three_d_b = [1, 0, 1]
    three_d_c = [1, 1, 3]
    three_d_d = [0, 1, 0]

    assert not adjacent(one_d_a, one_d_a)
    assert adjacent(one_d_a, one_d_b)
    assert not adjacent(one_d_a, one_d_c)

    assert not adjacent(two_d_a, two_d_a)
    assert adjacent(two_d_a, two_d_b)
    assert adjacent(two_d_a, two_d_c)
    assert not adjacent(two_d_a, two_d_d)

    assert not adjacent(three_d_a, three_d_a)
    assert adjacent(three_d_a, three_d_b)
    assert not adjacent(three_d_a, three_d_c)
    assert not adjacent(three_d_a, three_d_d)


def test_neighbours_does_not_include_self():
    y = 0
    x = 0
    z = 0
    r = 0
    c = 0
    point = (x, y, z)

    neighs_neighs = neighs(y, x)
    neighs_bounded_neighs = neighs_bounded(y, x, -10, 10, -10, 10)
    eight_neighs_neighs = eight_neighs(y, x)
    eight_neighs_bounded_neighs = eight_neighs_bounded(y, x, -10, 10, -10, 10)
    hexneighs_neighs = hexneighs(r, c)
    n_neighs_neighs = tuple(n_neighs(point))

    assert 4 == len(neighs_neighs)
    assert 4 == len(neighs_bounded_neighs)
    assert 8 == len(eight_neighs_neighs)
    assert 8 == len(eight_neighs_bounded_neighs)
    assert 6 == len(hexneighs_neighs)
    assert 26 == len(n_neighs_neighs)

    assert (y, x) not in neighs_neighs
    assert (y, x) not in neighs_bounded_neighs
    assert (y, x) not in eight_neighs_neighs
    assert (y, x) not in eight_neighs_bounded_neighs
    assert (r, c) not in hexneighs_neighs
    assert point not in n_neighs_neighs


def test_overlap():
    touching_begin_a = [1, 3]
    touching_begin_b = [3, 10]

    assert overlap(touching_begin_a, touching_begin_b)

    semicovered_a = [2, 7]
    semicovered_b = [5, 0]

    assert overlap(semicovered_a, semicovered_b)

    touching_end_a = [7, 11]
    touching_end_b = [11, 16]

    assert overlap(touching_end_a, touching_end_b)

    first_contained_a = [4, 9]
    first_contained_b = [2, 20]

    assert overlap(first_contained_a, first_contained_b)

    second_contained_a = [19, 28]
    second_contained_b = [21, 23]

    assert overlap(second_contained_a, second_contained_b)

    non_overlapping_a = [13, 20]
    non_overlapping_b = [33, 40]

    assert not overlap(non_overlapping_a, non_overlapping_b)


def test_words():
    line = 'A hh Fh2;j majkjags  36 u,u'

    assert ['A', 'hh', 'Fh', 'j', 'majkjags', 'u', 'u'] == words(line)


def test_between():
    assert between(10, 5, 15)
    assert between(10, 15, 5)
    assert not between(5, 5, 10)
    assert between(5, 5, 15, False)


def test_dimensions():
    grid_1_x_1 = [[1]]
    grid_2_x_3 = [[1,2,3],[4,5,6]]
    grid_3_x_2 = [[1,2],[3,4],[5,6]]

    assert (1, 1) == dimensions(grid_1_x_1)
    assert (2, 3) == dimensions(grid_2_x_3)
    assert (3, 2) == dimensions(grid_3_x_2)


def test_sum_of_differences():
    l = [-3, 0, 4, 4, 9]

    assert 56 == sum_of_differences(l)


def test_rim():    
    matrix = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16]
    ]

    matrim = rim(matrix)

    assert 12 == len(matrim)
    
    assert (0, 0, 1) in matrim 
    assert (0, 1, 2) in matrim
    assert (0, 2, 3) in matrim
    assert (0, 3, 4) in matrim
    assert (3, 0, 13) in matrim
    assert (3, 1, 14) in matrim
    assert (3, 2, 15) in matrim
    assert (3, 3, 16) in matrim
    assert (1, 0, 5) in matrim
    assert (2, 0, 9) in matrim
    assert (1, 3, 8) in matrim
    assert (2, 3, 12) in matrim


def test_junctions():
    simple_matrix = [
        '########',
        '#.#..#.#',
        '#.#.##.#',
        '#...#..#',
        '#.#.#.##',
        '#.#...##',
        '#.#.#..#',
        '########',
    ]

    complex_matrix = [
        '########',
        '#m#0p#o#',
        '#a#o##4#',
        '#eed#12#',
        '#f#1#4##',
        '#f#2po##',
        '#2#5#lk#',
        '########',
    ]

    simple_intersections = junctions(simple_matrix, None, '.')
    complex_intersections = junctions(complex_matrix, '#')

    assert simple_intersections == complex_intersections

    assert len(simple_intersections) == 4
    assert (3, 1) in simple_intersections
    assert (3, 3) in simple_intersections
    assert (5, 3) in simple_intersections
    assert (5, 5) in simple_intersections


def test_solve_system():
    system_a = [
        [1, 2, 5],
        [2, 4, 10]
    ]

    system_b = [
        [1, 2, 5, 10],
        [-2, 1, 3, 0],
        [-1, 3, 8, 10]
    ]

    system_c = [
        [1, 1, -3, 1, 2],
        [-5, 3, -4, 1, 0],
        [1, 0, 2, -1, 1],
        [1, 2, 0, 0, 12]
    ]

    asolves, _ = solve_system(system_a)
    bsolves, _ = solve_system(system_b)
    csolves, csolved = solve_system(system_c)

    assert not asolves
    assert not bsolves
    assert csolves

    a, x, y, z = csolved

    assert a == Fraction(22, 17)
    assert x == Fraction(91, 17)
    assert y == Fraction(84, 17)
    assert z == Fraction(173, 17)