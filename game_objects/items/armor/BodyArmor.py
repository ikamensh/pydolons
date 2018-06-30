from game_objects.items import Item, ItemTypes
from mechanics.damage import Armor

class BodyArmor(Item):
    def __init__(self, name, armor, durability, special_values = None):

        assert isinstance(armor, int)
        if special_values:
            assert isinstance(special_values, dict)

        super().__init__(name, durability)
        self.armor = Armor(base_value=armor, armor_dict=special_values)
        self.type = ItemTypes.BODY_ARMOR