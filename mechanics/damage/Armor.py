from mechanics.damage.DamageTypes import DamageTypes
from utils.numeric import clamp

class Armor:
    MIN_ARMOR = 0

    def __init__(self, armors_dict={}):
        self.armor_values = {}
        for dtype in DamageTypes:
            if dtype in armors_dict:
                self.armor_values[dtype] = max(armors_dict[dtype],
                                               Armor.MIN_ARMOR)
            else:
                self.armor_values[dtype] = 0


