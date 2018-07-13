from enum import Enum, auto

class BonusAttributes(Enum):
    HEALTH = auto()
    MANA = auto()
    STAMINA = auto()

    STR = auto()
    END = auto()
    PRC = auto()
    AGI = auto()
    INT = auto()
    CHA = auto()

def get_attrib_by_enum(unit, attrib):
    if attrib is BonusAttributes.STR:
        return unit.str
    if attrib is BonusAttributes.AGI:
        return unit.agi
    if attrib is BonusAttributes.INT:
        return unit.int
    if attrib is BonusAttributes.END:
        return unit.end
    if attrib is BonusAttributes.PRC:
        return unit.prc
    if attrib is BonusAttributes.CHA:
        return unit.cha

    if attrib is BonusAttributes.HEALTH:
        return unit.health
    if attrib is BonusAttributes.STAMINA:
        return unit.stamina
    if attrib is BonusAttributes.MANA:
        return unit.mana