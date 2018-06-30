from game_objects.items import Item
from GameLog import gamelog


class ItemTransactions:

    def __init__(self, unit):
        self.owner = unit
        self.equipment = unit.equipment
        self.inventory = unit.inventory
        self.manipulated_item = None

    def pickup(self, items):
        if isinstance(items, Item):
            single_item = items
            return self.inventory.add(single_item)

    def interact_with_equipment(self, slot):
        self.manipulated_item, self.inventory[slot] = self.inventory[slot], self.manipulated_item

    def interact_with_inventory(self, slot):
        self.manipulated_item, self.inventory[slot] = self.inventory[slot], self.manipulated_item

    def equip(self, slot):
        self.inventory[slot] = self.equipment.equip(self.inventory[slot])

    def drop_item(self, item):
        gamelog("{} dropped {}.".format(self.owner, item))

    def stop_manipulation(self):
        if self.manipulated_item:
            if self.pickup(self.manipulated_item):
                pass
            else:
                self.drop_item(self.manipulated_item)
            self.manipulated_item = None


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_manipulation()




