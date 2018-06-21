from game_objects.items.Item import Item

class Armor(Item):
    def __init__(self, armor, durability):
        Item.__init__(self,durability)
        self.armor = armor