from my_utils.named_enums import NameEnum, auto


class ItemTypes(NameEnum):
    BODY_ARMOR = auto()
    WEAPON = auto()
    HELMET = auto()
    BOOTS = auto()
    RING = auto()

    MATERIAL = auto()
    BLUEPRINT = auto()

    RUNE = auto()
    SPELL_CONCEPT = auto()
    SPELL = auto()

    CHARGED = auto()
