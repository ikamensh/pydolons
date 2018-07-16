from enum import Enum,auto
from game_objects.items import Item

class SlotTypes(Enum):
    BODY_ARMOR = auto()
    WEAPON = auto()
    HELMET = auto()
    BOOTS = auto()
    RING = auto()

class Slot:
    def __init__(self, name, item_type = None):
        self.name = name
        self.item_type = item_type
        self._content = None

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, item):
        if item:
            assert isinstance(item, Item)
            if self.item_type:
                assert item.item_type.slot == self.item_type
        if self.content:
            raise Exception("Remove existing item first.")

        self._content = item


    def swap_item(self, other_slot):
        self._content, other_slot._content = other_slot.content, self.content

    def take_content(self):
        item = self.content
        self._content = None
        return item


class StandardSlots:

    std_slots = [
        ("head", SlotTypes.HELMET),
        ("body", SlotTypes.BODY_ARMOR),
        ("hands", SlotTypes.WEAPON),
        ("feet", SlotTypes.BOOTS),
        ("ring1", SlotTypes.RING),
        ("ring2", SlotTypes.RING)
    ]

    @staticmethod
    def get_standard_slots():
        result = []
        for name, type in StandardSlots.std_slots:
            result.append(Slot(name, type))
        return result

