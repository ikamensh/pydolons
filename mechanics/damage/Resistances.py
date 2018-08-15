from mechanics.damage.DamageTypes import DamageTypes
from my_utils.utils import clamp

class Resistances:
    MAX_RESISTANCE = 0.95
    MAX_VULNERABILITY = -20

    def __init__(self, resists_dict=None):
        resists_in = resists_dict or {}
        self.resist_values = {}
        for dtype in DamageTypes:
            if dtype in resists_in:
                self.resist_values[dtype] = resists_in[dtype]
            else:
                self.resist_values[dtype] = 0

    def value(self):
        self.finalize()
        return self

    def finalize(self):
        for dtype in DamageTypes:
            self.resist_values[dtype] = clamp(self.resist_values[dtype],
                                             Resistances.MAX_VULNERABILITY,
                                             Resistances.MAX_RESISTANCE)

    def __getitem__(self, item):
        return self.resist_values[item]


    def __add__(self, other):
        result = {}
        for damage_type in self.resist_values.keys():
            result[damage_type] = self[damage_type] + other[damage_type]
        return Resistances(resists_dict=result)



