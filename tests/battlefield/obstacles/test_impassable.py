from mechanics.events import MovementEvent
from battlefield import Cell


def test_impassable_event(obstacle, hero, empty_game):

    empty_game.add_unit(hero, 1+1j)
    empty_game.add_obstacle(obstacle, 1+2j)

    MovementEvent(hero, 1+2j)

    assert empty_game.battlefield.unit_locations[hero] == 1+1j

def test_impassible_action(obstacle, hero, empty_game):


    empty_game.add_unit(hero, 1+1j, facing=1j)
    empty_game.add_obstacle(obstacle, 1+2j)

    tgt_cell = Cell(1,2)
    valid_action = None
    for a in hero.movement_actives:
        if a.check_target(tgt_cell):
            valid_action = a

    assert valid_action is None


import pytest
from exceptions import PydolonsException

def test_impassible_order(obstacle, hero, empty_game):


    empty_game.add_unit(hero, 1+1j, facing=1j)
    empty_game.add_obstacle(obstacle, 1+2j)

    tgt_cell = Cell(1,2)

    with pytest.raises(PydolonsException):
        empty_game.order_move(hero, tgt_cell)

    assert empty_game.battlefield.unit_locations[hero] == 1+1j