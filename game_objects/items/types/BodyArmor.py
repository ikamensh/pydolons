from game_objects.items import Item, ItemTypes
from mechanics.damage import Armor

class BodyArmor(Item):
    def __init__(self, name, armor, durability, blueprint, material, quality):

        assert isinstance(armor, Armor)
        super().__init__(name, item_type=ItemTypes.BODY_ARMOR, blueprint=blueprint, material=material, quality=quality, durability=durability)
        self.armor = armor