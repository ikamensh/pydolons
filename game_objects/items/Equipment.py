from game_objects.items import EquipmentSlotTypes
from game_objects.items import Item

class Equipment:
    slots = [EquipmentSlotTypes.WEAPON, EquipmentSlotTypes.BODY_ARMOR, EquipmentSlotTypes.BOOTS,
                  EquipmentSlotTypes.HELMET ]
    contents = {}

    def __init__(self):
        for slot in Equipment.slots:
            self.contents[slot] = None

    def __setitem__(self, slot, item):
        assert slot in self.contents
        if item:
            assert isinstance(item, Item)
            assert slot == item.type



    def equip(self, item):
        assert isinstance(item, Item)

        item_type = item.type
        slot = self[item_type]
        old_item = self[slot]
        self[slot] = item
        return old_item


