
def test_lightning_depends_on_mastery(game_hvsp, pirate_band, hero, lightning_active):

    hero.int_base += -50
    pirate = pirate_band[0]
    hp_before = pirate.health

    mana_before = hero.mana
    stamina_before = hero.stamina
    readiness_before = hero.readiness

    lightning_active = hero.give_active(lightning_active)


    hero.activate(lightning_active, pirate)
    #failed to activate - complexity mismatch
    assert mana_before == hero.mana
    assert stamina_before == hero.stamina
    assert readiness_before == hero.readiness

    assert pirate.health == hp_before

    hero.masteries.exp_spent[lightning_active.spell.school] += 1e9
    hero.activate(lightning_active, pirate)


    assert mana_before > hero.mana
    assert stamina_before > hero.stamina
    assert readiness_before > hero.readiness

    assert pirate.health < hp_before


def test_lightning_depends_on_int(hero, game_hvsp, pirate_band, lightning_active):

    hero.int_base += -50
    pirate = pirate_band[0]
    hp_before = pirate.health

    mana_before = hero.mana
    stamina_before = hero.stamina
    readiness_before = hero.readiness

    lightning_active = hero.give_active(lightning_active)


    hero.activate(lightning_active, pirate)
    # failed to activate - complexity mismatch

    assert mana_before == hero.mana
    assert stamina_before == hero.stamina
    assert readiness_before == hero.readiness

    assert pirate.health == hp_before

    hero.int_base += 100
    hero.activate(lightning_active, pirate)

    assert stamina_before > hero.stamina
    assert readiness_before > hero.readiness

    assert pirate.health < hp_before