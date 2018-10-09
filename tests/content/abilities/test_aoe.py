from cntent.abilities.aoe_damage import aoe_damage
import copy

from mechanics.damage import DamageTypes, Damage, ImpactFactor
from mechanics.events import DamageEvent



def test_aoe(empty_game, hero, pirate_band):

    hero.add_ability( aoe_damage(1,1)() )

    p1, p2, p3 = pirate_band

    empty_game.add_unit(p1, 2+2j, None)
    empty_game.add_unit(p2, 2+3j, None)
    empty_game.add_unit(p3, 3+4j, None)

    DamageEvent(Damage(100, DamageTypes.LIGHTNING), p2, source=hero, impact_factor=ImpactFactor.CRIT)

    assert p1.health < p1.max_health
    assert p3.health == p3.max_health







