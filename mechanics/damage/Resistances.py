from mechanics.damage.DamageTypes import DamageTypes
from utils.numeric import clamp

class Resistances:
    MAX_RESISTANCE = 0.95
    MAX_VULNERABILITY = -20

    def __init__(self, resists_dict={}):
        self.resist_values = {}
        for dtype in DamageTypes:
            if dtype in resists_dict:
                self.resist_values[dtype] = clamp(resists_dict[dtype],
                                                 Resistances.MAX_VULNERABILITY,
                                                 Resistances.MAX_RESISTANCE)
            else:
                self.resist_values[dtype] = 0


