from character.masteries.Masteries import Masteries
from game_objects.battlefield_objects import BaseType, Unit
from game_objects.monsters.MonsterEquipment import MonsterEquipment
import copy

class Monster:

    def __init__(self, base_type: BaseType, items = None, masteries : Masteries = None ):

        if items:
            if not isinstance(items, MonsterEquipment):
                items = MonsterEquipment(items)

        self.base_type = base_type
        self.items = items
        self.masteries = masteries


    def create(self, game, cell=None) -> Unit:
        unit = Unit(self.base_type, game=game, cell=cell)
        if self.items:
            self.items.random = game.random
            for item in self.items:
                unit.equipment.equip_item(item)

        if self.masteries:
            unit.masteries = copy.copy(self.masteries)
        else:
            unit.masteries = Masteries.max_out(self.base_type.xp, unit.melee_mastery)


        return unit

