from game_objects.battlefield_objects.Unit import Unit


from mechanics.combat.AttackEvent import AttackEvent


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
    def __attack(source : Unit, target : Unit, damage):
        event = AttackEvent(source, target, damage)
        return event.result



