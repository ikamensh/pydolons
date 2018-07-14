from content.triggers.upgrade_hits import upgrade_hits
from mechanics.damage import DamageEvent, Damage, DamageTypes
from mechanics.chances import ImpactFactor
import pytest


@pytest.mark.parametrize("n",[1,3,8])
def test_undead_n_hits(game, hero, n):

    trig = upgrade_hits(hero, n)
    damage_amount = 33
    dmg = Damage(damage_amount, DamageTypes.ACID)

    for _ in range(n):
        hp_before = hero.health
        DamageEvent(dmg, hero, source=hero, impact_factor=ImpactFactor.HIT)
        hp_after = hero.health
        assert hp_before - hp_after > damage_amount

    hp_before = hero.health
    DamageEvent(dmg, hero, source=hero, impact_factor=ImpactFactor.HIT)
    hp_after = hero.health
    assert hp_before - hp_after <= damage_amount

