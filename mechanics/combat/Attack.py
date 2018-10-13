from game_objects.battlefield_objects import BattlefieldObject, Unit
from mechanics.damage import Damage
from mechanics.events import AttackEvent




class Attack:

    @staticmethod
    def attack(game, source, target):
        weapon = source.get_melee_weapon()
        return AttackEvent(game, source, target, weapon)


    @staticmethod
    def expected_dmg(source: Unit, target:BattlefieldObject):
        weapon = source.get_melee_weapon()
        fake_event = AttackEvent(source, target, weapon, fire=False)
        chances = fake_event.calculate_chances()
        expected_dmg = Damage.calculate_expected_damage(chances, weapon.damage, target)
        return expected_dmg



