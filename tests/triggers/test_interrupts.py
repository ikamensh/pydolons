from content.triggers.immortality import immortality, undead_n_hits, refraction
from mechanics.damage import DamageEvent, Damage, DamageTypes
import pytest

def test_immortality(game, hero):

    trig = immortality(hero)
    dmg = Damage(200, DamageTypes.ACID)

    while hero.health > 0:
        DamageEvent(dmg,hero)

    assert hero.alive

    trig.deactivate()
    DamageEvent(dmg, hero)
    assert not hero.alive

@pytest.mark.parametrize("n",[1,3,8])
def test_undead_n_hits(game, hero, n):

    undead_n_hits(hero, n)

    dmg = Damage(200, DamageTypes.ACID)

    while hero.health > 0:
        DamageEvent(dmg, hero)

    assert hero.alive

    n_left = n-1
    for _ in range(n_left):
        DamageEvent(dmg, hero)

    assert hero.alive

    DamageEvent(dmg,hero)
    assert not hero.alive

@pytest.mark.parametrize("n",[1,3,8])
def test_refraction(game, hero, n):

    refraction(hero, n)

    dmg = Damage(200, DamageTypes.FROST)

    for _ in range(n):
        DamageEvent(dmg, hero)

    assert hero.health == hero.max_health

    DamageEvent(dmg, hero)
    assert hero.health < hero.max_health



