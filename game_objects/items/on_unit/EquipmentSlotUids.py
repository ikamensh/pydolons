from enum import auto

from my_utils.named_enums import NameEnum


class EquipmentSlotUids(NameEnum):
    HEAD = auto()
    BODY = auto()
    HANDS = auto()
    FEET = auto()
    RING_1 = auto()
    RING_2 = auto()

    # QUICK = auto()