from mechanics.actives import SingleUnitTargeting



def test_attack_cell(hero, pirate, lightning_active):

    hp_before = pirate.health

    mana_before = hero.mana
    stamina_before = hero.stamina
    readiness_before = hero.readiness

    hero.give_active(lightning_active)
    targeting = SingleUnitTargeting(pirate)

    hero.activate(lightning_active, targeting)

    assert mana_before > hero.mana
    assert stamina_before > hero.stamina
    assert readiness_before > hero.readiness

    assert pirate.health < hp_before