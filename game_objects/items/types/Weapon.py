from mechanics.damage import Damage
from game_objects.items import Item, ItemTypes

class Weapon(Item):
    def __init__(self, name, damage, durability, blueprint, material, quality):
        super().__init__(name, item_type=ItemTypes.WEAPON ,blueprint=blueprint, quality=quality, material=material, durability=durability)
        assert isinstance(damage, Damage)
        self.damage = damage