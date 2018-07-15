from utils.named_enums import NameEnum, auto

class AttributesEnum(NameEnum):
    STREINGTH = auto()
    ENDURANCE = auto()
    AGILITY = auto()
    PERCEPTION = auto()
    INTELLIGENCE = auto()
    CHARISMA = auto()

    HEALTH = auto()
    MANA = auto()
    STAMINA = auto()

abbrev_to_enum = {'str':AttributesEnum.STREINGTH, 'end':AttributesEnum.ENDURANCE, 'agi':AttributesEnum.AGILITY,
           'prc':AttributesEnum.PERCEPTION, 'int':AttributesEnum.INTELLIGENCE, 'cha':AttributesEnum.CHARISMA,
           'health':AttributesEnum.HEALTH, 'stamina': AttributesEnum.STAMINA, 'mana':AttributesEnum.MANA}

enum_to_abbrev = {v: k for k, v in abbrev_to_enum.items()}

def get_attrib_by_enum(unit, enum):
    name = enum_to_abbrev[enum]
    return getattr(unit, name)