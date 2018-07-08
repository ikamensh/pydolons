from mechanics.damage import deal_damage
from GameLog import gamelog

class Attack:
    @staticmethod
    def attack(source, target):
        gamelog("{} attacks {}.".format(source, target))
        damage = source.get_melee_damage()
        return deal_damage(damage, target)

    @staticmethod
    def unarmed_attack(source, target):
        gamelog("{} attacks {} with their bare hands.".format(source, target))
        damage = source.get_unarmed_damage()
        return deal_damage(damage, target)