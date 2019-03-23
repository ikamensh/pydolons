from battlefield.Vision import Vision
from battlefield.Facing import Facing
from battlefield.Cell import Cell
import pytest


f = Facing
@pytest.fixture(params=[f.NORTH, f.EAST, f.SOUTH, f.WEST])
def var_facing(request) -> complex:
    return request.param


@pytest.mark.parametrize('prc', [6, 10, 12, 17, 23, 29, 53, 113])
def test_symmetric(huge_game, hero, prc, var_facing):
    hero_c_coords = 30+30j

    huge_game.add_unit(hero, hero_c_coords, facing=var_facing)
    hero.prc_base.base = prc

    v = huge_game.vision
    print(hero.prc, hero.prc_base.base, hero.sight_range)
    cells_seen = v.std_seen_cells(hero)

    cells_to_right = set()
    cells_to_left = set()
    for c in cells_seen:
        vec = c.complex - hero_c_coords
        deg, ccw = Cell.angle_between(vec, var_facing)
        if deg > 1e-3:
            collection = cells_to_right if ccw else cells_to_left
            collection.add(c)

    assert len(cells_to_left) == len(cells_to_right)
    # pytest.skip("TODO: TEST INCOMPLETE. DIFFERENT SIGHT RANGES ARE NOT TESTED.")


def test_visibility(game_hvsp, hero):

    game_hvsp.add_unit(hero, cell=Cell(1,1), facing=Facing.SOUTH)

    cells_seen = game_hvsp.vision.std_seen_cells(hero)

    assert Cell(0,0) not in cells_seen
    assert Cell(7,7) not in cells_seen
    assert Cell(7,0) not in cells_seen
    assert Cell(0,7) not in cells_seen

    assert Cell(1,1) in cells_seen
    cell = Cell(1,int(1+hero.sight_range))
    print(cells_seen)
    assert cell in cells_seen
    cell = Cell(1+int(hero.sight_range),1)
    assert cell not in cells_seen


def test_borders(game_hvsp, hero):


    hero.facing = Facing.SOUTH
    hero.cell = Cell(1,1)

    vision = game_hvsp.vision
    cells_seen_before = vision.std_seen_cells(hero)


    hero.cell = Cell(7,7)
    cells_seen_after = vision.std_seen_cells(hero)

    assert len(cells_seen_after) < len(cells_seen_before)
    assert Cell(8,8) not in cells_seen_after

def test_direction_same_number(hero_only_game, hero):

    vision = hero_only_game.vision

    hero.facing = Facing.SOUTH
    hero.cell = Cell(4, 4)
    cells_seen_before = vision.std_seen_cells(hero)


    hero.facing = Facing.NORTH
    cells_seen_after = vision.std_seen_cells(hero)

    assert len(cells_seen_after) == len(cells_seen_before)
    assert cells_seen_before != cells_seen_after






