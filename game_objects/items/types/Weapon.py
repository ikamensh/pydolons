from mechanics.damage.Damage import Damage
from game_objects.items import WearableItem, ItemTypes
import copy

class Weapon(WearableItem):
    def __init__(self, name, damage, max_durability=None, *,  blueprint=None, material=None, quality=None):
        super().__init__(name, item_type=ItemTypes.WEAPON, blueprint=blueprint, quality=quality, material=material, max_durability=max_durability)
        assert isinstance(damage, Damage)
        self._damage = damage

    @property
    def damage(self):
        if self.max_durability is None:
            return copy.copy(self._damage)

        return Damage(self._damage.amount * self.durability_factor, self._damage.type)