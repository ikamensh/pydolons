from enum import Enum, auto

class DamageTypes(Enum):
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

    physical = {SLASH, CRUSH, PIERCE}
    elements = {FIRE, FROST, LIGHTNING, ACID}
    exotic = {SONIC, LIGHT}

