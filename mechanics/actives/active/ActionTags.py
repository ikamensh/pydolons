from enum import Enum, auto

class ActiveTags(Enum):
    MOVEMENT = auto()
    ATTACK = auto()
    MAGIC = auto()
    TURNING = auto()

    REST = auto()
    WAIT = auto()
    DEFEND = auto()

