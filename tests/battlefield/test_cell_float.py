from battlefield import Cell

class Foo:
    def __init__(self):
        pass

def test_cell():
    a = Cell(1.5, 2.0)
    b = Cell(2.5, 3.0)
    c = Cell(1.5, 2.0)
    f = Foo()
    f.x = 1.5
    f.y = 2.0

    assert (a == None) == False
    assert (a == f) == False
    assert (a == b) == False
    assert (a == c) == True
    assert (a == a) == True
