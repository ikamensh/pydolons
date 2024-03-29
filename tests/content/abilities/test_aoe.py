from cntent.abilities.aoe_damage.ability import aoe_damage

from mechanics.damage import DamageTypes, Damage, ImpactFactor
from mechanics.events import DamageEvent



def test_aoe(empty_game, hero, pirate_band):

    empty_game.add_unit(hero, 1+1j)
    ability = aoe_damage(1,1)()
    hero.add_ability( ability )

    p1, p2, p3 = pirate_band

    empty_game.add_unit(p1, 2+2j)
    empty_game.add_unit(p2, 2+3j)
    empty_game.add_unit(p3, 3+4j)

    DamageEvent(Damage(100, DamageTypes.LIGHTNING), p2, source=hero, impact_factor=ImpactFactor.CRIT)

    assert p1.health < p1.max_health
    assert p3.health == p3.max_health







