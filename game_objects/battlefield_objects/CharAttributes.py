from utils.named_enums import NameEnum, auto

class CharAttributes(NameEnum):
    STREINGTH = auto()
    ENDURANCE = auto()
    AGILITY = auto()
    PERCEPTION = auto()
    INTELLIGENCE = auto()
    CHARISMA = auto()

abbrevs = {'str':CharAttributes.STREINGTH, 'end':CharAttributes.ENDURANCE, 'agi':CharAttributes.AGILITY,
           'prc':CharAttributes.PERCEPTION, 'int':CharAttributes.INTELLIGENCE, 'cha':CharAttributes.CHARISMA}