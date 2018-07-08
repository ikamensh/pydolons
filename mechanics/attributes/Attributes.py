from enum import Enum, auto

class Attributes(Enum):
    HEALTH = auto()
    MANA = auto()
    STAMINA = auto()

    STR = auto()
    AGI = auto()
    INT = auto()

def get_attrib_by_enum(unit, attrib):
    if attrib is Attributes.STR:
        return unit.str
    if attrib is Attributes.AGI:
        return unit.agi
    if attrib is Attributes.INT:
        return unit.int

    if attrib is Attributes.HEALTH:
        return unit.health
    if attrib is Attributes.STAMINA:
        return unit.stamina
    if attrib is Attributes.MANA:
        return unit.mana