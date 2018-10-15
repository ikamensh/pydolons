from battlefield.Vision import Vision
from battlefield.Facing import Facing
from battlefield.Cell import Cell


def test_units_no_diag_block(hero, game_hvsp, pirate_band):

    bf = game_hvsp.battlefield
    bf.unit_locations = {}
    bf.units_at = {}
    bf.place(hero, Cell(1, 1))
    bf.unit_facings[hero] = Facing.SOUTH


    p1 = pirate_band[0]
    p2 = pirate_band[1]
    bf.place(p1, Cell(1, 2))
    bf.place(p2, Cell(2, 1))

    vision = Vision(bf)
    cells_seen = vision.std_seen_cells(hero)

    assert Cell(2, 2) in cells_seen

def test_walls_diag_block(hero, game_hvsp, steel_wall):

    bf = game_hvsp.battlefield
    bf.unit_locations = {}
    bf.units_at = {}
    bf.place(hero, Cell(1, 1))
    bf.unit_facings[hero] = Facing.SOUTH

    vision = Vision(bf)
    cells_seen = vision.std_seen_cells(hero)

    assert Cell(2, 2) in cells_seen


    bf.place(steel_wall(game_hvsp), Cell(1, 2))
    bf.place(steel_wall(game_hvsp), Cell(2, 1))

    cells_seen = vision.std_seen_cells(hero)

    assert Cell(2, 2) not in cells_seen