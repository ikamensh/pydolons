from game_objects.items import ItemTypes, Slot
from game_objects.items.on_unit.EquipmentSlotUids import EquipmentSlotUids

ss = EquipmentSlotUids

class StandardEquipment:

    std_slots = [
        (ss.HEAD, ItemTypes.HELMET),
        (ss.BODY, ItemTypes.BODY_ARMOR),
        (ss.HANDS, ItemTypes.WEAPON),
        (ss.FEET, ItemTypes.BOOTS),
        (ss.RING_1, ItemTypes.RING),
        (ss.RING_2, ItemTypes.RING)
    ]

    @staticmethod
    def get_standard_slots(owner):
        result = {}
        for uid, slot_type in StandardEquipment.std_slots:

            result[uid] = Slot( uid.name, slot_type, owner )

        return result