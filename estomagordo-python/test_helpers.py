from helpers import distance, distance_sq, ints, manhattan, neighs, neighs_bounded, columns, digits, chunks, chunks_with_overlap, positives, rays, rays_from_inside, adjacent, eight_neighs, eight_neighs_bounded, hexneighs, n_neighs


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