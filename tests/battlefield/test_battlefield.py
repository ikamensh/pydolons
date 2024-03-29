from battlefield.Battlefield import Cell
from battlefield.Facing import Facing
from game_objects.battlefield_objects import Wall

def test_movement_preserves_facing(game_hvsp, hero):

    for facing in [Facing.EAST, Facing.NORTH, Facing.WEST, Facing.SOUTH]:
        hero.facing = facing
        hero.cell = 1 + 1j
        assert hero.facing == facing


def test_units_dont_block_movement(game_hvsp, hero):
    location_before = Cell(3, 4)
    hero.cell = location_before

    assert game_hvsp.bf.cells_to_objs[Cell(4, 4)] # expecting a pirate from conftest

    game_hvsp.order_move(hero, Cell(4, 4))
    assert location_before != hero.cell

def test_walls_block_movement(empty_game, hero):
    location_before = Cell(3, 4)
    hero.cell = location_before
    empty_game.add_unit(hero)
    empty_game.bf.set_new_walls( [Wall(4+4j)] )

    empty_game.order_move(hero, Cell(4, 4))
    assert location_before == hero.cell

def test_distance_unit_to_point(game_hvsp):
    battlefield8 = game_hvsp.bf

    hero = battlefield8.get_objects_at(Cell(1, 1))[0]
    assert battlefield8.distance(hero, Cell(1, 4)) == 3

    pirate = battlefield8.get_objects_at(Cell(4, 4))[0]
    d1 = battlefield8.distance(pirate, Cell(1, 4))
    d2 =  battlefield8.distance(pirate, Cell(4, 1))
    assert d1 == d2

    assert battlefield8.distance(pirate, Cell(4, 4)) == 0

import pytest
from battlefield import Battlefield

@pytest.fixture()
def battlefield8():
    yield Battlefield(8,8)

def test_neighbouring_cells(battlefield8):
    battlefield8 = Battlefield(8, 8)

    #corners have 2 adjecent cells
    assert len(battlefield8.neighbours_exclude_center(Cell(0, 0))) == 2
    assert len(battlefield8.neighbours_exclude_center(Cell(0, 7))) == 2
    assert len(battlefield8.neighbours_exclude_center(Cell(7, 0))) == 2
    assert len(battlefield8.neighbours_exclude_center(Cell(7, 7))) == 2
    assert Cell(7, 6) in battlefield8.neighbours_exclude_center(Cell(7, 7))
    assert Cell(6, 7) in battlefield8.neighbours_exclude_center(Cell(7, 7))

    # top and side have 3 adjecent cells
    assert len(battlefield8.neighbours_exclude_center(Cell(0, 4))) == 3
    assert len(battlefield8.neighbours_exclude_center(Cell(5, 7))) == 3
    assert Cell(6, 7) in battlefield8.neighbours_exclude_center(Cell(5, 7))
    assert Cell(4, 7) in battlefield8.neighbours_exclude_center(Cell(5, 7))
    assert Cell(5, 6) in battlefield8.neighbours_exclude_center(Cell(5, 7))

    # usual cells have 4 adjecent cells
    assert len(battlefield8.neighbours_exclude_center(Cell(2, 4))) == 4
    assert len(battlefield8.neighbours_exclude_center(Cell(5, 3))) == 4
    assert Cell(6, 3) in battlefield8.neighbours_exclude_center(Cell(5, 3))
    assert Cell(4, 3) in battlefield8.neighbours_exclude_center(Cell(5, 3))
    assert Cell(5, 2) in battlefield8.neighbours_exclude_center(Cell(5, 3))
    assert Cell(5, 4) in battlefield8.neighbours_exclude_center(Cell(5, 3))


def test_cells_within_dist(battlefield8):
    assert len(battlefield8.get_cells_within_dist(Cell(4, 4), distance=1)) == 5
    assert len(battlefield8.get_cells_within_dist(Cell(4, 4), distance=1.5)) == 9
    assert len(battlefield8.get_cells_within_dist(Cell(4, 4), distance=2)) == 13
    assert len(battlefield8.get_cells_within_dist(Cell(4, 4), distance=2.5)) == 21
    assert len(battlefield8.get_cells_within_dist(Cell(4, 4), distance=2.99)) == 25
    assert len(battlefield8.get_cells_within_dist(Cell(4, 4), distance=3)) == 29





def test_distance_calc(battlefield8):
    p1 = Cell(1,1)
    p2 = Cell(1,2)

    assert battlefield8.distance(p1, p2) == 1

    p1 = Cell(1, 1)
    p2 = Cell(1, 3)

    assert battlefield8.distance(p1, p2) == 2

    p1 = Cell(1, 1)
    p2 = Cell(2, 2)

    assert 1 < battlefield8.distance(p1, p2) < 2



def test_cells_eq():
    cell1 = Cell(1, 1)
    cell2 = Cell(1, 1)
    assert cell1 == cell2


