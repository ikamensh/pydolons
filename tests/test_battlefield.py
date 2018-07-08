from battlefield.Battlefield import Cell, Battlefield
import pytest


@pytest.fixture()
def battlefield(pirate_band, hero):
    bf = Battlefield(8, 8)
    locations = [Cell(4, 4), Cell(4, 5), Cell(5, 4)]

    units_locations = {pirate_band[i]: locations[i] for i in range(3)}
    units_locations[hero] = Cell(1, 1)
    bf.place_many(units_locations)
    yield bf


def test_valid_placement(battlefield):
    assert len(battlefield.unit_locations) == 4
    for pirate in battlefield.unit_locations:
        assert pirate in battlefield.units_at.values()

def test_distance_unit_to_point(battlefield):
    hero = battlefield.get_unit_at(Cell(1,1))
    assert battlefield.distance_unit_to_point(hero, Cell(1,4)) == 3

    pirate = battlefield.get_unit_at(Cell(4,4))
    d1 = battlefield.distance_unit_to_point(pirate, Cell(1, 4))
    d2 =  battlefield.distance_unit_to_point(pirate, Cell(4, 1))
    assert d1 == d2

    assert battlefield.distance_unit_to_point(pirate, Cell(4,4)) == 0


def test_neighbouring_cells(battlefield):
    #corners have 2 adjecent cells
    assert len(battlefield.get_neighbouring_cells(Cell(0, 0))) == 2
    assert len(battlefield.get_neighbouring_cells(Cell(0, 7))) == 2
    assert len(battlefield.get_neighbouring_cells(Cell(7, 0))) == 2
    assert len(battlefield.get_neighbouring_cells(Cell(7, 7))) == 2
    assert Cell(7, 6) in battlefield.get_neighbouring_cells(Cell(7, 7))
    assert Cell(6, 7) in battlefield.get_neighbouring_cells(Cell(7, 7))

    # top and side have 3 adjecent cells
    assert len(battlefield.get_neighbouring_cells(Cell(0, 4))) == 3
    assert len(battlefield.get_neighbouring_cells(Cell(5, 7))) == 3
    assert Cell(6, 7) in battlefield.get_neighbouring_cells(Cell(5, 7))
    assert Cell(4, 7) in battlefield.get_neighbouring_cells(Cell(5, 7))
    assert Cell(5, 6) in battlefield.get_neighbouring_cells(Cell(5, 7))

    # usual cells have 4 adjecent cells
    assert len(battlefield.get_neighbouring_cells(Cell(2, 4))) == 4
    assert len(battlefield.get_neighbouring_cells(Cell(5, 3))) == 4
    assert Cell(6, 3) in battlefield.get_neighbouring_cells(Cell(5, 3))
    assert Cell(4, 3) in battlefield.get_neighbouring_cells(Cell(5, 3))
    assert Cell(5, 2) in battlefield.get_neighbouring_cells(Cell(5, 3))
    assert Cell(5, 4) in battlefield.get_neighbouring_cells(Cell(5, 3))


def test_cells_within_dist(battlefield):
    assert len(battlefield.get_cells_within_dist(Cell(4, 4), distance=1)) == 5
    assert len(battlefield.get_cells_within_dist(Cell(4, 4), distance=1.5)) == 9
    assert len(battlefield.get_cells_within_dist(Cell(4,4), distance=2)) == 13
    assert len(battlefield.get_cells_within_dist(Cell(4, 4), distance=2.5)) == 21
    assert len(battlefield.get_cells_within_dist(Cell(4, 4), distance=2.99)) == 25
    assert len(battlefield.get_cells_within_dist(Cell(4, 4), distance=3)) == 29






def test_distance_calc(battlefield):
    p1 = Cell(1,1)
    p2 = Cell(1,2)

    assert battlefield.distance(p1, p2) == 1

    p1 = Cell(1, 1)
    p2 = Cell(1, 3)

    assert battlefield.distance(p1, p2) == 2

    p1 = Cell(1, 1)
    p2 = Cell(2, 2)

    assert 1 < battlefield.distance(p1, p2) < 2





def test_cells_eq():
    cell1 = Cell(1, 1)
    cell2 = Cell(1, 1)
    assert cell1 == cell2


