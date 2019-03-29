from game_objects.items import Slot
from game_objects.items.on_unit.slot_groups.SlotGroup import SlotGroup


class Inventory(SlotGroup):

    @staticmethod
    def slot_name_at(i):
        return "inventory_{0:00d}".format(i)

    def __init__(self, max_capacity, owner):
        all_slots = [Slot(Inventory.slot_name_at(i), owner=owner)
                     for i in range(max_capacity)]
        super().__init__(all_slots, owner)
