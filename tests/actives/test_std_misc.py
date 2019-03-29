from cntent.actives.std.std_misc import onguard_active, rest_active, wait_active


def test_wait(empty_game, hero):
    empty_game.add_unit(hero, 1 + 1j)

    units_active = hero.give_active(wait_active)

    rdy_before = hero.readiness
    hero.activate(units_active)

    assert rdy_before > hero.readiness


def test_rest(empty_game, hero):
    empty_game.add_unit(hero, 1 + 1j)

    units_active = hero.give_active(rest_active)

    rdy_before = hero.readiness

    hero.mana -= 200
    mana_before = hero.mana

    hero.stamina -= 200
    stamina_before = hero.stamina

    attk_before = hero.melee_precision
    def_before = hero.melee_evasion

    hero.activate(units_active)

    assert rdy_before > hero.readiness

    # resting restores mana and stamina
    assert mana_before < hero.mana
    assert stamina_before < hero.stamina

    # resting weakens temporarily
    assert attk_before > hero.melee_precision
    assert def_before > hero.melee_evasion

    empty_game.turns_manager.pass_time(5)

    # after some time attk and def back to normal
    assert attk_before == hero.melee_precision
    assert def_before == hero.melee_evasion


def test_rest_debuff_temporary(empty_game, hero):
    empty_game.add_unit(hero, 1 + 1j)

    units_active = hero.give_active(rest_active)

    attk_before = hero.melee_precision
    def_before = hero.melee_evasion

    hero.activate(units_active)

    empty_game.turns_manager.pass_time(50)

    # after some time attk and def back to normal
    assert attk_before == hero.melee_precision
    assert def_before == hero.melee_evasion


def test_onguard(empty_game, hero):
    empty_game.add_unit(hero, 1 + 1j)

    units_active = hero.give_active(onguard_active)

    attk_before = hero.melee_precision
    def_before = hero.melee_evasion

    hero.activate(units_active)

    assert attk_before < hero.melee_precision
    assert def_before < hero.melee_evasion

    empty_game.turns_manager.pass_time(50)

    # after some time attk and def back to normal
    assert attk_before == hero.melee_precision
    assert def_before == hero.melee_evasion
