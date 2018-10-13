

def test_regen(game_hvsp, hero):
    assert hero in game_hvsp.turns_manager.managed
    assert hero in game_hvsp.battlefield.unit_locations.keys()


    hero.health -= 100
    hero.mana -= 100
    hero.stamina -= 100

    health_before = hero.health
    mana_before = hero.mana
    stamina_before = hero.stamina


    game_hvsp.turns_manager.pass_time(3)

    assert hero.health > health_before
    assert hero.mana > mana_before
    assert hero.stamina > stamina_before


def test_bleeding(game_hvsp, hero):
    assert hero in game_hvsp.turns_manager.managed
    assert hero in game_hvsp.battlefield.unit_locations.keys()


    hero.health -= 0.75 * hero.health

    health_before = hero.health


    game_hvsp.turns_manager.pass_time(3)

    assert hero.health < health_before


from cntent.monsters.undead import zombie

def test_undead_no_regen(empty_game):
    zomb = zombie.create()
    empty_game.add_unit(zomb, 1+1j, None)

    zomb.health -= 100
    health_before = zomb.health

    empty_game.turns_manager.pass_time(3)

    assert zomb.health == health_before

    zomb.health -= 200
    health_before = zomb.health

    empty_game.turns_manager.pass_time(3)

    assert zomb.health == health_before