from __future__ import annotations
from typing import List, TYPE_CHECKING
from mechanics.events import ItemDroppedEvent
if TYPE_CHECKING:
    from game_objects.items import Slot
    from game_objects.battlefield_objects import Unit


class SlotGroup:

    def __init__(self, all_slots: List[Slot], owner: Unit):
        self.all_slots = all_slots
        self.owner = owner

    @property
    def all_items(self):
        return [slot.content for slot in self.all_slots if slot.content]

    @property
    def empty_slots(self):
        return [slot for slot in self.all_slots if not slot.content]

    def get_empty_slot(self):
        for slot in self.all_slots:
            if not slot.content:
                return slot

    def add_from(self, slot):
        empty = self.get_empty_slot()
        if empty:
            empty.swap_item(slot)
            return True
        else:
            return False

    def add(self, item):
        if not self.empty_slots:
            ItemDroppedEvent(item)
            return False
        slot = self.empty_slots[0]
        slot.content = item
        return True

    def __getitem__(self, item):
        return self.all_slots[item]

    def drop(self, key):
        self[key].drop()

    def __iter__(self):
        return iter(self.all_slots)

    def __len__(self):
        return len(self.all_slots)
