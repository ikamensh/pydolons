from game_objects.items import Slot

class Inventory:

    @staticmethod
    def slot_name_at(i):
        return "inventory_{0:00d}".format(i)

    def __init__(self, max_capacity, owner):
        self.all = [Slot(Inventory.slot_name_at(i)) for i in range(max_capacity)]
        self.max_capacity = max_capacity
        self.owner = owner

    def __setitem__(self, slot_num, item):
        slot = self.all[slot_num]
        slot.content = item

    def __getitem__(self, slot_num):
        return self.all[slot_num].content

    def __len__(self):
        count = sum([1 for slot in self.all if slot.content])
        return count

    @property
    def empty_slots(self):
        return [slot for slot in self.all if not slot.content]

    def get_empty_slot(self):
        for slot in self.all:
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
            return False
        slot = self.empty_slots[0]
        slot.content = item
        return True

    def drop(self, slot_num):
        slot = self.all[slot_num]
        if slot.content:
            slot.pop_item()



