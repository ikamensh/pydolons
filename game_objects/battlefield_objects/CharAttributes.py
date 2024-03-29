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

c = CharAttributes

core_attributes = [c.STREINGTH,
                   c.ENDURANCE,
                   c.AGILITY,
                   c.PERCEPTION,
                   c.INTELLIGENCE,
                   c.CHARISMA]

abbrev_to_enum = {'str':c.STREINGTH, 'end':c.ENDURANCE, 'agi':c.AGILITY,
           'prc':c.PERCEPTION, 'int':c.INTELLIGENCE, 'cha':c.CHARISMA,
           'health':c.HEALTH, 'stamina': c.STAMINA, 'mana':c.MANA,
                  'initiative':c.INITIATIVE, 'armor':c.ARMOR, 'resistances':c.RESISTANCES,
                  'melee_precision': c.PRECISION, 'melee_evasion': c.EVASION}

base_attributes = [c.STREINGTH, c.ENDURANCE, c.AGILITY, c.PERCEPTION, c.INITIATIVE, c.CHARISMA]

enum_to_abbrev = {v: k for k, v in abbrev_to_enum.items()}

def get_attrib_by_enum(unit, enum):
    name = enum_to_abbrev[enum]
    return getattr(unit, name)

class Constants:
    HP_PER_END = 25
    STAMINA_PER_STR = 5
    MANA_PER_INT = 10
    UNARMED_DAMAGE_PER_STR = 3

std_bonus = Attribute(1, 0.05, 2)

value_norms = {
    **{attr: std_bonus*1 for attr in core_attributes},
    c.HEALTH : std_bonus*2*Constants.HP_PER_END,
    c.MANA: std_bonus*2*Constants.MANA_PER_INT,
    c.STAMINA: std_bonus*2*Constants.STAMINA_PER_STR,
    c.INITIATIVE : std_bonus*0.2
}