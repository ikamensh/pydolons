from game_objects.battlefield_objects.Unit import Unit


from mechanics.combat.AttackEvent import AttackEvent


class Attack:
    #Once weapons are implemented: get damage by weapon, pass weapon to attack event.

    @staticmethod
    def attack(source, target):
        weapon = source.get_melee_weapon()
        return Attack.__attack(source, target, weapon)



    @staticmethod
    def __attack(source : Unit, target : Unit, weapon):
        AttackEvent(source, target, weapon)



