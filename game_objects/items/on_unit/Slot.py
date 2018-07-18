from game_objects.items import Item, ItemTypes

class Slot:
    def __init__(self, name, item_type = None, owner = None):
        self.name = name
        self.item_type = item_type
        self.owner = owner
        self._content = None

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, item):
        if item:
            assert isinstance(item, Item)
            if self.item_type:
                assert item.item_type is self.item_type
        if self.content:
            raise Exception("Remove existing item first.")

        self._content = item
        item.slot = self
        item.owner = self.owner



    def swap_item(self, other_slot):
        self._content, other_slot._content = other_slot.content, self.content

    def pop_item(self):
        item = self.content
        self._content = None
        return item


class StandardSlots:

    std_slots = [
        ("head", ItemTypes.HELMET),
        ("body", ItemTypes.BODY_ARMOR),
        ("hands", ItemTypes.WEAPON),
        ("feet", ItemTypes.BOOTS),
        ("ring1", ItemTypes.RING),
        ("ring2", ItemTypes.RING)
    ]

    @staticmethod
    def get_standard_slots(owner):
        result = []
        for name, type in StandardSlots.std_slots:
            result.append(Slot(name, type, owner))
        return result

