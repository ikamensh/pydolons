from cntent.triggers.damage_to_attacker import damage_to_attackers
from mechanics.combat import Attack
from mechanics.damage import Damage, DamageTypes

def test_damage_to_attackers(game_hvsp, hero, pirate_band):
    trig = damage_to_attackers(hero, hero, Damage(15, DamageTypes.FIRE))
    for pirate in pirate_band:
        Attack.attack(pirate, hero)
        assert pirate.health < pirate.max_health

    trig.deactivate()

    health_before = [pirate.health for pirate in pirate_band]
    for pirate in pirate_band:
        Attack.attack(pirate, hero)

    assert [pirate.health for pirate in pirate_band] == health_before


def test_interrupting_damage_to_attackers(game_hvsp, hero, pirate_band, no_chances):
    trig = damage_to_attackers(hero, hero, Damage(1500, DamageTypes.LIGHTNING), interrupt=True)
    for pirate in pirate_band:
        Attack.attack(pirate, hero)
        assert not pirate.alive
        assert hero.health == hero.max_health
        break

    trig.deactivate()

    alive_band = [pirate for pirate in pirate_band if pirate.alive]

    health_before = [pirate.health for pirate in alive_band]
    for pirate in alive_band:
        hero_hp_before = hero.health
        Attack.attack(pirate, hero)
        assert hero.health < hero_hp_before

    assert [pirate.health for pirate in alive_band] == health_before
