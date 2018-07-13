from collections import namedtuple
from mechanics.events.Event import DamageDealtEvent
from mechanics.PrecisionEvasion.CritHitGrazeMiss import ImpactFactor, effect_coef, protection_coef

Damage = namedtuple("Damage", "amount type")

def deal_damage(damage, target,*, source=None, impact_factor=ImpactFactor.HIT):
    dmg_type = damage.type
    damage_dealt = calculate_damage(damage, target, impact_factor)
    target_died = target.lose_health(damage_dealt)
    DamageDealtEvent(source, target, impact_factor, damage_dealt, dmg_type)

    return target_died

def calculate_damage(damage, target, impact_factor=ImpactFactor.HIT):
    dmg_type = damage.type

    resist = target.resists[dmg_type]
    armor = target.armor[dmg_type] * protection_coef[impact_factor]

    damage_final = int(   max( (damage.amount - armor) * (1 - resist), 0) * effect_coef[impact_factor])
    return damage_final

