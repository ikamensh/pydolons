from collections import namedtuple
from GameLog import gamelog

Damage = namedtuple("Damage", "amount type")

def deal_damage(damage, target):

    type = damage.type

    resist = target.resists[type]
    armor = target.armor[type]

    damage_dealt = int ( (damage.amount - armor) * (1 - resist) )
    if damage_dealt <= 0 :
        gamelog("{} laughs at the attempts to damage it with {}".format(target, type))
        return False

    target_died = target.lose_health(damage_dealt)
    log_message = "{} recieves {} {} damage.".format(target, damage_dealt, type)
    if target_died:
        log_message += "{} dies.".format(target)
    gamelog(log_message)
    return target_died

