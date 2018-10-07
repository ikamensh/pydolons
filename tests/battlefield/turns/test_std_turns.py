from cntent.actives.std_movements import turn_cw, turn_ccw
from battlefield import Facing


def test_turn_cw(hero, game):

    game.battlefield.unit_facings[hero] = Facing.NORTH
    _turn_cw = hero.give_active(turn_cw)
    _turn_cw.activate()
    assert game.battlefield.unit_facings[hero] == Facing.EAST
    _turn_cw.activate()
    assert game.battlefield.unit_facings[hero] == Facing.SOUTH
    _turn_cw.activate()
    assert game.battlefield.unit_facings[hero] == Facing.WEST
    _turn_cw.activate()
    assert game.battlefield.unit_facings[hero] == Facing.NORTH


def test_turn_ccw(hero, game):

    game.battlefield.unit_facings[hero] = Facing.NORTH
    _turn_ccw = hero.give_active(turn_ccw)

    _turn_ccw.activate()
    assert game.battlefield.unit_facings[hero] == Facing.WEST
    _turn_ccw.activate()
    assert game.battlefield.unit_facings[hero] == Facing.SOUTH
    _turn_ccw.activate()
    assert game.battlefield.unit_facings[hero] == Facing.EAST
    _turn_ccw.activate()
    assert game.battlefield.unit_facings[hero] == Facing.NORTH