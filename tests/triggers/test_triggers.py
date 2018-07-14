from content.triggers.damage_to_attacker import damage_to_attackers
from mechanics.combat import Attack

def test_damage_to_attackers(game, hero, pirate_band):
    trig = damage_to_attackers(hero, hero)
    for pirate in pirate_band:
        Attack.attack(pirate, hero)
        assert pirate.health < pirate.max_health

    trig.deactivate()

    health_before = [pirate.health for pirate in pirate_band]
    for pirate in pirate_band:
        Attack.attack(pirate, hero)

    assert [pirate.health for pirate in pirate_band] == health_before
