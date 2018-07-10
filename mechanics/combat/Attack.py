from mechanics.damage import deal_damage
from mechanics.events.Event import AttackStartedEvent

class Attack:
    #Once weapons are implemented: get damage by weapon, pass weapon to attack event.

    @staticmethod
    def attack(source, target):
        damage = source.get_melee_damage()
        return Attack.__attack(source, target, damage)

    @staticmethod
    def unarmed_attack(source, target):
        damage = source.get_unarmed_damage()
        return Attack.__attack(source,target,damage)


    @staticmethod
    def __attack(source, target, damage):
        AttackStartedEvent(source, target)
        return deal_damage(damage, target, source=source)

