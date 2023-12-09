day1 = __import__('1')
day2 = __import__('2')
day3 = __import__('3')
day4 = __import__('4')
day5 = __import__('5')
day6 = __import__('6')
day7 = __import__('7')


def test_day1():
    a, b = day1.main()
    
    assert a == 54239
    assert b == 55343


def test_day2():
    a, b = day2.main()
    
    assert a == 2101
    assert b == 58269


def test_day3():
    a, b = day3.main()
    
    assert a == 537832
    assert b == 81939900


def test_day4():
    a, b = day4.main()
    
    assert a == 25004
    assert b == 14427616


def test_day5():
    a, b = day5.main()
    
    assert a == 650599855
    assert b == 1240035


def test_day6():
    a, b = day6.main()
    
    assert a == 131376
    assert b == 34123437


def test_day7():
    a, b = day7.main()
    
    assert a == 248836197
    assert b == 251195607