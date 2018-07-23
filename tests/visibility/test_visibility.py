from battlefield.Vision import Vision
from battlefield.Facing import Facing
from battlefield.Cell import Cell

def test_visibility(game, hero):

    bf = game.battlefield

    bf.move(hero, Cell(1,1))
    assert bf.unit_facings[hero] is Facing.NORTH

    vision = Vision(bf)
    cells_seen = vision.std_seen_cells(hero)

    assert Cell(0,0) not in cells_seen
    assert Cell(7,7) not in cells_seen
    assert Cell(7,0) not in cells_seen
    assert Cell(0,7) not in cells_seen

    assert Cell(1,1) in cells_seen
    assert Cell(1,int(1+hero.sight_range)) in cells_seen
    assert Cell(1+int(hero.sight_range),1) not in cells_seen


def test_borders(game, hero):

    bf = game.battlefield
    assert bf.unit_facings[hero] is Facing.NORTH

    bf.move(hero, Cell(1, 1))
    vision = Vision(bf)
    cells_seen_before = vision.std_seen_cells(hero)


    bf.move(hero, Cell(7, 7))
    cells_seen_after = vision.std_seen_cells(hero)

    assert len(cells_seen_after) < len(cells_seen_before)
    assert Cell(8,8) not in cells_seen_after

def test_direction(game, hero):

    bf = game.battlefield
    assert bf.unit_facings[hero] is Facing.NORTH

    vision = Vision(bf)
    bf.unit_locations = {}
    bf.units_at = {}
    bf.place(hero, Cell(4, 4))
    cells_seen_before = vision.std_seen_cells(hero)


    bf.unit_facings[hero] = Facing.SOUTH
    cells_seen_after = vision.std_seen_cells(hero)

    assert len(cells_seen_after) == len(cells_seen_before)
    assert cells_seen_before != cells_seen_after






