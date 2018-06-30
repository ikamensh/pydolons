from game_objects.items import EquipmentSlotTypes

class ItemType:
    def __init__(self, slot_type = None):
        self.slot = slot_type

class ItemTypes:
    WEAPON = ItemType(EquipmentSlotTypes.WEAPON)
    BODY_ARMOR = ItemType(EquipmentSlotTypes.BODY_ARMOR)
    GENERIC = ItemType()
