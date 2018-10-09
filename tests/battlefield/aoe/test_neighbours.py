from battlefield.Cell import Cell
import pytest

def test_neighbours():
    c = Cell(5,5)

    assert len(Cell.get_neighbours(c, distance=0)) == 1
    assert len(Cell.get_neighbours(c, distance=1)) == 5
    assert len(Cell.get_neighbours(c, distance=1.5)) == 9
    assert len(Cell.get_neighbours(c, distance=2)) == 13

@pytest.mark.parametrize("w, h", [(1,1), (1,5), (5,2), (33,1), (16,17), (4,4)])
def test_borders(w,h):
    c = Cell(2,2)

    all_valid_cells = Cell.get_neighbours(c, distance=500, w=w,h=h)
    assert len(all_valid_cells) == w*h
    min_x, max_x = min([c.x for c in all_valid_cells]), max([c.x for c in all_valid_cells])
    min_y, max_y = min([c.y for c in all_valid_cells]), max([c.y for c in all_valid_cells])

    assert min_x == min_y == 0
    assert max_x == w-1
    assert max_y == h-1