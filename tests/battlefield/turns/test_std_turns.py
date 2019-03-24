from cntent.actives.std.std_movements import turn_cw, turn_ccw
from battlefield import Facing


def test_turn_cw(hero, game_hvsp):

    hero.facing = Facing.NORTH
    _turn_cw = hero.give_active(turn_cw)
    _turn_cw.activate()
    assert hero.facing == Facing.EAST
    _turn_cw.activate()
    assert hero.facing == Facing.SOUTH
    _turn_cw.activate()
    assert hero.facing == Facing.WEST
    _turn_cw.activate()
    assert hero.facing == Facing.NORTH


def test_turn_ccw(hero, game_hvsp):

    hero.facing = Facing.NORTH
    _turn_ccw = hero.give_active(turn_ccw)

    _turn_ccw.activate()
    assert hero.facing == Facing.WEST
    _turn_ccw.activate()
    assert hero.facing == Facing.SOUTH
    _turn_ccw.activate()
    assert hero.facing == Facing.EAST
    _turn_ccw.activate()
    assert hero.facing == Facing.NORTH