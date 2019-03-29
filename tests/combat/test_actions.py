from battlefield.Battlefield import Cell
from battlefield.Facing import Facing
from exceptions.PydolonsError import PydolonsError
import pytest


def test_move(game_hvsp, hero):
    initial_location = hero.cell

    target_location = Cell(1, 2)
    hero.readiness = 1.09
    game_hvsp.order_move(hero, target_location)
    assert initial_location != hero.cell
    assert target_location == hero.cell


def test_facing_no_problem(game_hvsp, hero):
    initial_location = hero.cell

    hero.facing = Facing.NORTH

    target_location = Cell(1, 2)
    hero.readiness = 1.09
    try:
        for _ in range(10):
            game_hvsp.order_move(hero, target_location)
    except PydolonsError as e:
        pass

    assert initial_location != hero.cell
    assert target_location == hero.cell


def test_can_make_multiple_steps(game_hvsp, hero):
    initial_location = hero.cell

    hero.facing = Facing.NORTH

    target_location = Cell(0, 6)
    hero.readiness = 1.09
    try:
        for _ in range(20):
            game_hvsp.order_move(hero, target_location)
            hero.readiness = 1.09
    except PydolonsError as e:
        pass

    assert initial_location != hero.cell
    assert target_location == hero.cell


def test_can_use_diag_step(game_hvsp, hero):
    initial_location = hero.cell
    hero.facing = Facing.SOUTH

    target_location = Cell(2, 2)
    hero.readiness = 1.09
    game_hvsp.order_move(hero, target_location)

    assert initial_location != hero.cell
    assert target_location == hero.cell


def test_go_and_hit(game_hvsp, hero):
    """
    Hero goes to the pirate and kicks pirate.
    He kicks him until pirate has hp.
    Pirate dies, hero can and does step on the tile where pirate stood.
    """
    pirate_location = Cell(4, 4)
    the_enemy_pirate = game_hvsp.bf.get_objects_at(pirate_location)[0]
    hero.readiness = 1

    path = [Cell(c[0], c[1]) for c in [(1, 2), (2, 2), (2, 3), (3, 3), (3, 4)]]
    try:
        for step in path:
            game_hvsp.order_move(hero, step)
            hero.readiness = 1

        while the_enemy_pirate.health > 0:
            game_hvsp.order_attack(hero, pirate_location)
            hero.readiness = 1

        game_hvsp.order_move(hero, pirate_location)
    except Exception as e:
        print(e)
        assert False

    assert pirate_location == hero.cell
