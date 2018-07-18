from utils.named_enums import NameEnum, auto

class DamageTypes(NameEnum):
    SLASH = auto()
    CRUSH = auto()
    PIERCE = auto()

    FIRE = auto()
    FROST = auto()
    LIGHTNING = auto()
    ACID = auto()

    # design: succeptable entities have strong vulnerability. damage of below types comes in small amounts.
    SONIC = auto()

class DamageTypeGroups:
    physical = {DamageTypes.SLASH, DamageTypes.CRUSH, DamageTypes.PIERCE}
    elemental = {DamageTypes.FIRE, DamageTypes.FROST, DamageTypes.LIGHTNING, DamageTypes.ACID}
    exotic = {DamageTypes.SONIC}

if __name__ == "__main__":
    print(list(DamageTypes))