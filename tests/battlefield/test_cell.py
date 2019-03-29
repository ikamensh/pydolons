from battlefield import Cell


class Foo:
    def __init__(self):
        pass


def test_cell():
    a = Cell(1, 2)
    b = Cell(2, 3)
    c = Cell(1, 2)
    f = Foo()
    f.x = 1
    f.y = 2

    assert (a is None) == False
    assert (a == f) == False
    assert (a == b) == False
    assert (a == c)
    assert (a == a)
