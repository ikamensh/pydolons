from game_objects.items import WearableItem, ItemTypes
from mechanics.damage import Armor
import copy

class BodyArmor(WearableItem):
    def __init__(self, name, armor, max_durability, *, blueprint=None, material=None, quality=None):

        assert isinstance(armor, Armor)
        super().__init__(name, item_type=ItemTypes.BODY_ARMOR, blueprint=blueprint, material=material, quality=quality, max_durability=max_durability)
        self._armor = armor

    @property
    def armor(self):
        if self.max_durability is None:
            return copy.copy(self._armor)
        else:
            return self._armor * self.durability_factor

    def __repr__(self):
        return f"{self.name} providing {self.armor} armor"

