from mechanics import events
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_objects.battlefield_objects import BattlefieldObject, Unit




class RangedAttack:

    @staticmethod
    def ranged_attack(source, target):
        weapon = source.get_ranged_weapon()
        assert weapon is not None
        return events.RangedAttackEvent(source, target, weapon)


    # @staticmethod
    # def expected_dmg(source: Unit, target:BattlefieldObject):
    #     weapon = source.get_melee_weapon()
    #     fake_event = AttackEvent(source, target, weapon, fire=False)
    #     chances = fake_event.calculate_chances()
    #     expected_dmg = Damage.expected(chances, weapon.damage, target)
    #     return expected_dmg



