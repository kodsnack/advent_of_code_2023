class Pos2D:
    def __init__(self, x, y):
        assert isinstance(x, int)
        assert isinstance(y, int)
        self._x = x
        self._y = y
    @property
    def x(self):
        return self._x
    @property
    def y(self):
        return self._y
    def __add__(self, rhs):
        assert isinstance(rhs, Pos2D)
        return Pos2D(self.x + rhs.x, self.y + rhs.y)
    def __sub__(self, rhs):
        assert isinstance(rhs, Pos2D)
        return Pos2D(self.x + rhs.x, self.y + rhs.y)
    def __mul__(self, rhs):
        assert isinstance(rhs, int)
        return Pos2D(self.x * rhs, self.y * rhs)
    def north(self):
        return Pos2D(self.x, self.y - 1)
    def south(self):
        return Pos2D(self.x, self.y + 1)
    def west(self):
        return Pos2D(self.x - 1, self.y)
    def east(self):
        return Pos2D(self.x + 1, self.y)
    def left(self):
        return Pos2D(self.y, -self.x)
    def right(self):
        return Pos2D(-self.y, self.x)
    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, Pos2D) and self.x == rhs.x and self.y == rhs.y
    def __lt__(self, rhs) -> bool:
        return self.y < rhs.y or self.y == rhs.y and self.x < rhs.x
    def __str__(self):
        return f"({self.x}, {self.y})"
    def __repr__(self):
        return f"Pos2D({self.x}, {self.y})"
    def __hash__(self):
        return (self.x, self.y).__hash__()
    def __neg__(self):
        return Pos2D(-self.x, -self.y)
    def manhattan(self, rhs):
        assert isinstance(rhs, Pos2D)
        return abs(self.x - rhs.x) + abs(self.y - rhs.y)

def test_left_rotation():
    pos = Pos2D(1, 0)
    pos = pos.left()
    assert pos == Pos2D(0, -1)
    pos = pos.left()
    assert pos == Pos2D(-1, 0)
    pos = pos.left()
    assert pos == Pos2D(0, 1)
    pos = pos.left()
    assert pos == Pos2D(1, 0)

def test_right_rotation():
    pos = Pos2D(1, 0)
    pos = pos.right()
    assert pos == Pos2D(0, 1)
    pos = pos.right()
    assert pos == Pos2D(-1, 0)
    pos = pos.right()
    assert pos == Pos2D(0, -1)
    pos = pos.right()
    assert pos == Pos2D(1, 0)

def test_moves():
    pos = Pos2D(3, 4)
    pos = pos.north()
    assert pos == Pos2D(3, 3)
    pos = pos.west()
    assert pos == Pos2D(2, 3)
    pos = pos.south()
    assert pos == Pos2D(2, 4)
    pos = pos.east()
    assert pos == Pos2D(3, 4)