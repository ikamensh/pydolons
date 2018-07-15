from battlefield.Battlefield import Cell


def test_move(game, hero):
    initial_location = game.get_location(hero)

    target_location = Cell(1, 2)
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

    for step in path:
        step_done = game.order_move(hero,step)
        assert step_done

    location_before = game.get_location(hero)
    hp_before = the_enemy_pirate.health
    game.order_move(hero, pirate_location)
    assert location_before == game.get_location(hero)

    while the_enemy_pirate.health > 0:
        game.order_move(hero, pirate_location)

    game.order_move(hero, pirate_location)
    assert pirate_location == game.get_location(hero)
