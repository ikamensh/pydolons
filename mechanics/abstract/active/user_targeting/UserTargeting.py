from enum import Enum, auto
class UserTargetingType(Enum):
    TARGET_UNIT = auto()
    TARGET_CELL = auto()

class UserTargeting:
    def __init__(self, target):
        self.target = target
