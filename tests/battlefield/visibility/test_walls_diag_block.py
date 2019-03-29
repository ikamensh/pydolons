from game_objects.battlefield_objects import Wall
from battlefield.Vision import Vision
from battlefield.Facing import Facing
from battlefield.Cell import Cell


def test_units_no_diag_block(hero, empty_game, pirate_band):

    empty_game.add_unit(hero, Cell(1, 1))
    hero.facing = Facing.SOUTH

    p1 = pirate_band[0]
    p2 = pirate_band[1]
    empty_game.add_unit(p1, Cell(1, 2))
    empty_game.add_unit(p2, Cell(2, 1))

    cells_seen = empty_game.vision.std_seen_cells(hero)

    assert Cell(2, 2) in cells_seen


def test_walls_diag_block(hero, empty_game, steel_wall):

    empty_game.add_unit(hero, Cell(1, 1))
    hero.facing = Facing.SOUTH

    cells_seen = empty_game.vision.std_seen_cells(hero)

    assert Cell(2, 2) in cells_seen

    empty_game.bf.set_new_walls([Wall(Cell(1, 2)), Wall(Cell(2, 1))])
    cells_seen = empty_game.vision.std_seen_cells(hero)

    assert Cell(2, 2) not in cells_seen
