from game_objects.items import Item, ItemTypes


class Rune(Item):
    def __init__(self, bonuses, name="Mysterious Rune"):
        super().__init__(name, ItemTypes.SPELL)
        self.bonuses = bonuses
