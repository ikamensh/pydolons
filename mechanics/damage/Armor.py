from mechanics.damage.DamageTypes import DamageTypes

class Armor:
    MIN_ARMOR = 0

    def __init__(self, base_value = 0, armor_dict=None):
        self.armor_values = {}
        for dtype in DamageTypes:
            self[dtype] = base_value
        if armor_dict:
            self.armor_values.update(armor_dict)


    def value(self):
        self.finalize()
        return self


    def finalize(self):
        for k,v in self.armor_values.items():
            if v < Armor.MIN_ARMOR:
                self[k] = Armor.MIN_ARMOR


    def __setitem__(self, key, value):
        assert isinstance(key, DamageTypes)
        self.armor_values.__setitem__(key, int(value) )

    def __getitem__(self, item):
        return self.armor_values[item]

    def __add__(self, other):
        result = {}
        for damage_type in self.armor_values.keys():
            result[damage_type] = self[damage_type] + other[damage_type]
        return Armor(armor_dict=result)

    def __mul__(self, other):
        assert other < 1e20 # is a number

        result = {}
        for damage_type in self.armor_values.keys():
            result[damage_type] = self[damage_type] * other
        return Armor(armor_dict=result)

    def values(self):
        return self.armor_values.values()

    def keys(self):
        return self.armor_values.keys()

    def items(self):
        return self.armor_values.items()

    def display_value(self):
        return sum(self.values()) / len(self.values())

    def __repr__(self):
        return f"{self.display_value() :.0f}"

