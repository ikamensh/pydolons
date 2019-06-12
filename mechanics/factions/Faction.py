from enum import Enum, auto

class Faction(Enum):
    PLAYER = auto()
    ALLY = auto()
    ENEMY = auto()
    NEUTRALS = auto()

from collections import defaultdict

f = Faction

allegiances = {
    f.PLAYER:{f.PLAYER:1, f.ALLY:0.8, f.ENEMY:-1, f.NEUTRALS:0},
    f.ALLY:{f.PLAYER:0.5, f.ALLY:0.2, f.ENEMY:-1, f.NEUTRALS:0},
    f.ENEMY:{f.PLAYER:-1, f.ALLY:-0.2, f.ENEMY:1, f.NEUTRALS:0},
    f.NEUTRALS: defaultdict(lambda: 0)
               }

