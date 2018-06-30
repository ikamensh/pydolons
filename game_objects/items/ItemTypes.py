from game_objects.items import SlotTypes

class ItemType:
    def __init__(self, slot_type = None):
        self.slot = slot_type

class ItemTypes:
    WEAPON = ItemType(SlotTypes.WEAPON)
    BODY_ARMOR = ItemType(SlotTypes.BODY_ARMOR)
    GENERIC = ItemType()
