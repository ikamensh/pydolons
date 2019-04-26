from __future__ import annotations
from mechanics import damage
from mechanics import events
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_objects.battlefield_objects import BattlefieldObject, Unit


class Attack:

    @staticmethod
    def melee_attack(source, target):
        weapon = source.get_melee_weapon()
        return events.AttackEvent(source, target, weapon)


    @staticmethod
    def expected_dmg(source: Unit, target: BattlefieldObject):
        weapon = source.get_melee_weapon()
        fake_event = events.AttackEvent(source, target, weapon, fire=False)
        chances = fake_event.calculate_chances()
        expected_dmg = damage.Damage.expected(chances, weapon.damage, target)
        return expected_dmg



