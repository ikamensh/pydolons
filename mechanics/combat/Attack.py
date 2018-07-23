from game_objects.battlefield_objects import Unit
from mechanics.combat.AttackEvent import AttackEvent




class Attack:

    @staticmethod
    def attack(source, target):
        weapon = source.get_melee_weapon()
        return Attack.__attack(source, target, weapon)



    @staticmethod
    def __attack(source : Unit, target : Unit, weapon):

        AttackEvent(source, target, weapon)



