from game_objects.items import StandardSlots, ItemTypes, WearableItem
import itertools


class Equipment:
    def __init__(self, owner):
        self.contents = StandardSlots.get_standard_slots(owner)
        self.map = {slot.name : slot for slot in self.contents}
        self.slots_per_type = {st:[] for st in ItemTypes}
        for slot in self.contents:
            type = slot.item_type
            self.slots_per_type[type].append(slot)

        self.owner = owner


    @property
    def equiped_items(self):
        return [slot.content for slot in self.contents if slot.content is not None]

    @property
    def bonuses(self):
        return itertools.chain.from_iterable([item.bonuses for item in self.equiped_items])

    def remove_item(self, slot):
        return slot.pop_item()

    def __setitem__(self, slot_name, item):
        self.map[slot_name].content = item

    def __getitem__(self, slot_name):
        return self.map[slot_name].content

    def unequip_item(self, item):
        for slot in self.contents:
            if slot.content is item:
                slot.pop_item()
                self.owner.inventory.add(item)
                self.owner.recalc()
                return


    def equip_item(self, item):

        if not isinstance(item, WearableItem):
            return False

        slot_type = item.item_type

        if slot_type is None:
            return False

        all_slots_of_type = self.slots_per_type[slot_type]
        if not all_slots_of_type:
            return False

        empty_slots_of_type = [slot for slot in all_slots_of_type if not slot.content]

        if empty_slots_of_type:
            chosen_slot = empty_slots_of_type[0]
            chosen_slot.content = item
            self.owner.recalc()
            return True
        else:
            if self.owner.inventory.add_from(all_slots_of_type[0]):
                all_slots_of_type[0].content = item
                self.owner.recalc()
                return True
            else:
                return False



    def equip(self, slot_from):
        """
        Choose a fitting slot, and exchange items with it.
        """

        item = slot_from.content
        if not isinstance(item, WearableItem):
            return False

        slot_type = item.item_type
        if slot_type is None:
            return False

        all_slots_of_type = self.slots_per_type[slot_type]
        if not all_slots_of_type:
            return False

        empty_slots_of_type = [slot for slot in all_slots_of_type if not slot.content]

        if empty_slots_of_type:
            chosen_slot = empty_slots_of_type[0]
        else:
            chosen_slot = all_slots_of_type[0]

        chosen_slot.swap_item(slot_from)
        self.owner.recalc()
        return True


