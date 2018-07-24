from content.actives.std_movements import turn_cw, turn_ccw
from battlefield import Facing


def test_turn_cw(hero, game):

    game.battlefield.unit_facings[hero] = Facing.NORTH
    hero.give_active(turn_cw)
    turn_cw.activate()
    assert game.battlefield.unit_facings[hero] == Facing.EAST
    turn_cw.activate()
    assert game.battlefield.unit_facings[hero] == Facing.SOUTH
    turn_cw.activate()
    assert game.battlefield.unit_facings[hero] == Facing.WEST
    turn_cw.activate()
    assert game.battlefield.unit_facings[hero] == Facing.NORTH


def test_turn_ccw(hero, game):

    game.battlefield.unit_facings[hero] = Facing.NORTH
    hero.give_active(turn_ccw)

    turn_ccw.activate()
    assert game.battlefield.unit_facings[hero] == Facing.WEST
    turn_ccw.activate()
    assert game.battlefield.unit_facings[hero] == Facing.SOUTH
    turn_ccw.activate()
    assert game.battlefield.unit_facings[hero] == Facing.EAST
    turn_ccw.activate()
    assert game.battlefield.unit_facings[hero] == Facing.NORTH