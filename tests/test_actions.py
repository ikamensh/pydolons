from tests.resources.dungeons import demo_dungeon
from Game import Game
from game_objects.battlefield_objects.Unit.base_types.demo_hero import demohero_basetype
from game_objects.battlefield_objects.Unit.Unit import Unit
from battlefield.Battlefield import Coordinates



def test_move():
    hero = Unit(demohero_basetype)
    game = Game(demo_dungeon, hero)

    initial_location = game.get_location(hero)

    target_location = Coordinates(1,2)
    game.order_move(hero, target_location)
    assert initial_location != game.get_location(hero)
    assert target_location == game.get_location(hero)

def test_go_and_hit():
    """
    Hero goes to the pirate and kicks pirate.
    He kicks him until pirate has hp.
    Pirate dies, hero can and does step on the tile where pirate stood.
    :return:
    """
    hero = Unit(demohero_basetype)
    game = Game(demo_dungeon, hero)

    pirate_location = Coordinates(4,4)
    the_enemy_pirate = game.get_unit_at(pirate_location)

    path = [Coordinates(c[0], c[1]) for c in [(1,2),(2,2),(2,3),(3,3),(3,4)]]

    for step in path:
        step_done = game.order_move(hero,step)
        assert step_done

    location_before = game.get_location(hero)
    hp_before = the_enemy_pirate.health
    game.order_move(hero, pirate_location)
    assert location_before == game.get_location(hero)
    assert the_enemy_pirate.health < hp_before

    while the_enemy_pirate.health > 0:
        game.order_move(hero, pirate_location)

    game.order_move(hero, pirate_location)
    assert pirate_location == game.get_location(hero)
