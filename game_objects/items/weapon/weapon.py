from game_objects.items.Item import Item

class Weapon(Item):
    def __init__(self, damage, durability):
        Item.__init__(self,durability)
        self.damage = damage