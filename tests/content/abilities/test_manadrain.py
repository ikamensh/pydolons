from cntent.abilities.mana_drain.ability import mana_drain

from mechanics.damage import DamageTypes, Damage, ImpactFactor
from mechanics.events import DamageEvent


def test_drain_heal(empty_game, hero, pirate):

    empty_game.add_unit(hero, 1 + 1j)
    hero.add_ability(mana_drain(20, 0.05, 0.5)())

    empty_game.add_unit(pirate, 2 + 2j)

    hero.health -= 100

    pirate_mana_before = pirate.mana

    hero_health_before = hero.health

    DamageEvent(Damage(100, DamageTypes.LIGHTNING), pirate,
                source=hero, impact_factor=ImpactFactor.HIT)

    assert pirate.mana < pirate_mana_before
    assert hero.health > hero_health_before
