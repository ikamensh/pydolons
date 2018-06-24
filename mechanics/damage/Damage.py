from collections import namedtuple

Damage = namedtuple("Damage", "amount type")

def deal_damage(damage, target):
    type = damage.type
    resist = target.resist[type]
    armor = target.armor[type]
    damage_dealt = int ( (damage.amount - armor) * (1 - resist) )
    target_died = target.recieve_damage(damage_dealt)
    log_message = "{} recieves {} {} damage.".format(target, damage_dealt, type)
    if target_died:
        log_message += "{} dies.".format(target)
    return target_died

