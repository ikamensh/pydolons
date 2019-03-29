from game_objects.items import Slot, ItemTypes
from game_objects.items.on_unit.slot_groups.SlotGroup import SlotGroup


class QuickItems(SlotGroup):

    @staticmethod
    def slot_name_at(i):
        return "Quick item {0:0d}".format(i)

    def __init__(self, max_capacity, owner):
        all_slots = [
            Slot(
                self.slot_name_at(i),
                item_type=ItemTypes.CHARGED,
                owner=owner) for i in range(max_capacity)]
        super().__init__(all_slots, owner)
