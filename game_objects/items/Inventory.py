from game_objects.items import Item

class Inventory(dict):

    def __init__(self, max_capacity):
        super().__init__()
        self.empty = list(range(1,max_capacity+1))
        self.valid_positions = set(self.empty)

    def __setitem__(self, slot, item):
        old_item = self[slot]
        assert slot in self.valid_positions
        if item:
            assert isinstance(item, Item)
        else:
            self.empty.append(slot)
        super().__setitem__(slot, item)
        return old_item

    def add(self, item):
        if not self.empty:
            return False

        slot = self.empty[-1]
        assert self[slot] is None
        self[slot] = item
        self.empty.remove(slot)
        return True

    def drop(self, slot):
        self[slot] = None



