from battlefield.Battlefield import Cell
import pytest

def test_move(game, hero):
    initial_location = game.get_location(hero)

    target_location = Cell(1, 2)
    game.order_move(hero, target_location)
    assert initial_location != game.get_location(hero)
    assert target_location == game.get_location(hero)

def test_facing_no_problem(game, hero):
    initial_location = game.get_location(hero)

    game.battlefield.unit_facings[hero] = 0-1j

    target_location = Cell(1, 2)
    try:
        for _ in range(10):
            game.order_move(hero, target_location)
    except:
        pass

    assert initial_location != game.get_location(hero)
    assert target_location == game.get_location(hero)


def test_can_make_multiple_steps(game, hero):
    initial_location = game.get_location(hero)

    game.battlefield.unit_facings[hero] = 0-1j

    target_location = Cell(0, 6)
    try:
        for _ in range(20):
            game.order_move(hero, target_location)
    except:
        pass

    assert initial_location != game.get_location(hero)
    assert target_location == game.get_location(hero)

def test_can_use_diag_step(game, hero):
    initial_location = game.get_location(hero)

    target_location = Cell(2, 2)
    game.order_move(hero, target_location)

    assert initial_location != game.get_location(hero)
    assert target_location == game.get_location(hero)

def test_go_and_hit(game, hero):
    """
    Hero goes to the pirate and kicks pirate.
    He kicks him until pirate has hp.
    Pirate dies, hero can and does step on the tile where pirate stood.
    """
    pirate_location = Cell(4, 4)
    the_enemy_pirate = game.get_unit_at(pirate_location)

    path = [Cell(c[0], c[1]) for c in [(1, 2), (2, 2), (2, 3), (3, 3), (3, 4)]]
    try:
        for step in path:
            game.order_move(hero,step)


        while the_enemy_pirate.health > 0:
            game.order_attack(hero, pirate_location)

        game.order_move(hero, pirate_location)
    except Exception as e:
        assert False, repr(e)

    assert pirate_location == game.get_location(hero)


