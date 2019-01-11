from __future__ import annotations
from game_objects.items import StandardEquipment, ItemTypes, WearableItem, EquipmentSlotUids
from game_objects.items.on_unit.slot_groups.SlotGroup import SlotGroup
import itertools
from typing import Dict, Union, TYPE_CHECKING
from mechanics.events import ItemDroppedEvent
if TYPE_CHECKING:
    from game_objects.items import Slot


class Equipment(SlotGroup):
    def __init__(self, owner):
        self.map : Dict[EquipmentSlotUids, Slot] = StandardEquipment.get_standard_slots(owner)
        all_slots = [v for k,v in self.map.items()]
        self.slots_per_type = {st:[] for st in ItemTypes}
        for slot in all_slots:
            slot_type = slot.item_type
            self.slots_per_type[slot_type].append(slot)

        super().__init__(all_slots, owner)

    @property
    def bonuses(self):
        return itertools.chain.from_iterable([item.bonuses for item in self.all_items])

    def equip_item(self, item) -> bool:
        """
        :param item: item to equip
        :return: boolean: success?
        """

        # if not isinstance(item, WearableItem):
        #     return False # item can't be equiped

        slot_type = item.item_type

        if slot_type is None:
            return False # item can't be equiped

        all_slots_of_type = self.slots_per_type[slot_type]
        if not all_slots_of_type:
            return False # owner does not have a slot for this type of item

        empty_slots_of_type = [slot for slot in all_slots_of_type if not slot.content]

        if empty_slots_of_type:
            chosen_slot = empty_slots_of_type[0]
            chosen_slot.content = item
            self.owner.recalc()
            return True # item was put into an empty slot
        else:
            if self.owner.inventory.add_from(all_slots_of_type[0]):
                all_slots_of_type[0].content = item
                self.owner.recalc()
                return True # replaced an item
            else:
                return False # slot is occupied, inventory is full: can't equip

    def equip(self, slot_from: Slot):
        item = slot_from.pop_item()
        return self.equip_item(item)


    def unequip_slot(self, slot):
        if isinstance(slot, EquipmentSlotUids):
            slot = self.map[slot]

        assert slot in self.all_slots
        item = slot.pop_item()

        inv = self.owner.inventory
        if not inv.add(item):
            ItemDroppedEvent(item)

    def unequip_item(self, item):
        for slot in self.all_slots:
            if slot.content is item:
                self.unequip_slot(slot)


    def __getitem__(self, item):
        return self.map[item].content







