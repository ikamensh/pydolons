from game_objects.attributes import Attribute
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

    ARMOR = auto()
    RESISTANCES = auto()

    PRECISION = auto()
    EVASION = auto()

abbrev_to_enum = {'str':CharAttributes.STREINGTH, 'end':CharAttributes.ENDURANCE, 'agi':CharAttributes.AGILITY,
           'prc':CharAttributes.PERCEPTION, 'int':CharAttributes.INTELLIGENCE, 'cha':CharAttributes.CHARISMA,
           'health':CharAttributes.HEALTH, 'stamina': CharAttributes.STAMINA, 'mana':CharAttributes.MANA,
                  'initiative':CharAttributes.INITIATIVE, 'armor':CharAttributes.ARMOR, 'resistances':CharAttributes.RESISTANCES,
                  'melee_precision': CharAttributes.PRECISION, 'melee_evasion': CharAttributes.EVASION}

enum_to_abbrev = {v: k for k, v in abbrev_to_enum.items()}

def get_attrib_by_enum(unit, enum):
    name = enum_to_abbrev[enum]
    return getattr(unit, name)

class Constants:
    HP_PER_STR = 25
    STAMINA_PER_END = 5
    MANA_PER_INT = 10
    UNARMED_DAMAGE_PER_STR = 3

c = CharAttributes
std_bonus = Attribute(1, 0.05, 2)

value_norms = {
    c.STREINGTH : std_bonus*1,
    c.ENDURANCE: std_bonus*1,
    c.AGILITY: std_bonus*1,
    c.PERCEPTION: std_bonus*1,
    c.INTELLIGENCE: std_bonus*1,
    c.CHARISMA: std_bonus*1,
    c.HEALTH : std_bonus*2*Constants.HP_PER_STR,
    c.MANA: std_bonus*2*Constants.MANA_PER_INT,
    c.STAMINA: std_bonus*2*Constants.STAMINA_PER_END,
    c.INITIATIVE : std_bonus*0.2
}