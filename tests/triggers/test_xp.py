from mechanics.rpg.experience import exp_rule
from mechanics.events.combat.DamageEvent import DamageEvent
from mechanics.damage import DamageTypes, Damage



def test_gain_xp_by_kill(game_hvsp, hero, pirate_band):

    exp_rule(game_hvsp)

    pirate = pirate_band[0]

    hero.xp = 500
    xp_before = hero.xp

    DamageEvent(Damage(5000, DamageTypes.PIERCE), pirate, source=hero)

    xp_after = hero.xp

    assert xp_after > xp_before


def test_no_exp_weak_enemy(game_hvsp, hero, pirate_band):

    exp_rule(game_hvsp)

    pirate = pirate_band[0]

    hero.xp = 1e9
    xp_before = hero.xp

    DamageEvent(Damage(5000, DamageTypes.PIERCE), pirate, source=hero)

    xp_after = hero.xp

    assert xp_after == xp_before


def test_no_xp_foreign_kill(game_hvsp, hero, pirate_band):

    exp_rule(game_hvsp)

    pirate = pirate_band[0]

    hero.xp = 500
    xp_before = hero.xp

    DamageEvent(Damage(5000, DamageTypes.PIERCE), pirate)

    xp_after = hero.xp

    assert xp_after == xp_before