from collections import namedtuple
from mechanics.events.Event import DamageDealtEvent

Damage = namedtuple("Damage", "amount type")

def deal_damage(damage, target,*, source=None):
    dmg_type = damage.type
    damage_dealt = calculate_damage(damage, target)
    target_died = target.lose_health(damage_dealt)
    DamageDealtEvent(source, target, damage_dealt, dmg_type)

    return target_died

def calculate_damage(damage, target):
    dmg_type = damage.type

    resist = target.resists[dmg_type]
    armor = target.armor[dmg_type]

    damage_final = max( int((damage.amount - armor) * (1 - resist)), 0)
    return damage_final

