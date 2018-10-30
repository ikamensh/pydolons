from enum import Enum, auto

class ActiveTags(Enum):
    MOVEMENT = auto()
    TURNING = auto()

    ATTACK = auto()
    RANGED = auto()
    MAGIC = auto()

    RESTORATION = auto()
    WAIT = auto()
    DEFEND = auto()

    CHARGED_ITEM = auto()

