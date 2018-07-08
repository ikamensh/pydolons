from utils.named_enums import AutoName, auto

class DamageTypes(AutoName):
    SLASH = auto()
    CRUSH = auto()
    PIERCE = auto()

    FIRE = auto()
    FROST = auto()
    LIGHTNING = auto()
    ACID = auto()

    # design: succeptable entities have strong vulnerability. damage of below types comes in small amounts.
    SONIC = auto()
    LIGHT = auto()
    MIND = auto()

class DamageTypeGroups:
    physical = {DamageTypes.SLASH, DamageTypes.CRUSH, DamageTypes.PIERCE}
    elemental = {DamageTypes.FIRE, DamageTypes.FROST, DamageTypes.LIGHTNING, DamageTypes.ACID}
    exotic = {DamageTypes.SONIC, DamageTypes.LIGHT}

if __name__ == "__main__":
    print(list(DamageTypes))