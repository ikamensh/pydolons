from my_utils.named_enums import NameEnum, auto

class CharAttributes(NameEnum):
    STREINGTH = auto()
    ENDURANCE = auto()
    AGILITY = auto()
    PERCEPTION = auto()
    INTELLIGENCE = auto()
    CHARISMA = auto()

    HEALTH = auto()
    MANA = auto()
    STAMINA = auto()
    INITIATIVE = auto()

abbrev_to_enum = {'str':CharAttributes.STREINGTH, 'end':CharAttributes.ENDURANCE, 'agi':CharAttributes.AGILITY,
           'prc':CharAttributes.PERCEPTION, 'int':CharAttributes.INTELLIGENCE, 'cha':CharAttributes.CHARISMA,
           'health':CharAttributes.HEALTH, 'stamina': CharAttributes.STAMINA, 'mana':CharAttributes.MANA,
                  'initiative':CharAttributes.INITIATIVE}

enum_to_abbrev = {v: k for k, v in abbrev_to_enum.items()}

def get_attrib_by_enum(unit, enum):
    name = enum_to_abbrev[enum]
    return getattr(unit, name)