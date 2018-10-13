from game_objects.items import Item, Slot

class ItemTransactions:

    def __init__(self, unit):
        self.owner = unit
        self.equipment = unit.equipment
        self.inventory = unit.inventory
        self.manipulation_slot = Slot("Manipulated item")

    def pickup(self, container):
        if isinstance(container, Slot):
            slot = container
            return self.inventory.add_from(slot)
        else:
            for slot in container:
                if not self.inventory.add_from(slot):
                    return False
            return True


    def take_from(self, slot):
        self.manipulation_slot.swap_item(slot)

    def equip(self, slot):
        assert slot in self.inventory.all
        self.equipment.equip(slot)

    def drop_item(self, slot):
        # gamelog("{} dropped {}.".format(self.owner, slot.pop_item()))
        print("{} dropped {}.".format(self.owner, slot.pop_item()))

    def stop_manipulation(self):
        if self.manipulation_slot:
            if self.pickup(self.manipulation_slot):
                pass
            else:
                self.drop_item(self.manipulation_slot)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_manipulation()




