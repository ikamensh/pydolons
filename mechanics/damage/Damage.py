from collections import namedtuple
from GameLog import gamelog

Damage = namedtuple("Damage", "amount type")

def deal_damage(damage, target):
    dmg_type = damage.type
    damage_dealt = calculate_damage(damage, target)
    if damage_dealt == 0 :
        gamelog("{} laughs at the attempts to damage it with {}".format(target, dmg_type))
        return False

    target_died = target.lose_health(damage_dealt)
    log_message = "{} recieves {} {} damage.".format(target, damage_dealt, dmg_type)
    if target_died:
        log_message += " {} dies.".format(target)
    gamelog(log_message)
    return target_died

def calculate_damage(damage, target):
    dmg_type = damage.type

    resist = target.resists[dmg_type]
    armor = target.armor[dmg_type]

    damage_final = max( int((damage.amount - armor) * (1 - resist)), 0)
    return damage_final

