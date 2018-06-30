from mechanics.damage import DamageTypes
from game_objects.items import Item, ItemTypes

class Weapon(Item):
    def __init__(self, damage, damage_type, durability):
        assert damage_type in DamageTypes
        assert isinstance(damage, int)

        super().__init__(durability)
        self.damage = damage
        self.damage_type = damage_type
        self.type = ItemTypes.WEAPON