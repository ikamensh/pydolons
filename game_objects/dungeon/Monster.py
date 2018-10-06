from character_creation.Masteries import Masteries
from game_objects.battlefield_objects import BaseType, Unit
import copy

class Monster:

    def __init__(self, base_type: BaseType, item_groups, masteries : Masteries):
        self.base_type = base_type
        self.item_groups = item_groups
        self.masteries = masteries


    def create(self) -> Unit:
        unit = Unit(self.base_type)
        for item in self.item_groups:
            unit.equipment.equip_item(item)

        unit.masteries = copy.copy(self.masteries)


        return unit

