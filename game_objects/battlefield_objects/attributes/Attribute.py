class Attribute:
    def __init__(self, base, multiplier, bonus):
        self.base = base
        self.multiplier = multiplier
        self.bonus = bonus

    def __add__(self, other):
        new_base = self.base + other.base
        new_multiplier = self.multiplier + other.multiplier
        new_bonus = self.bonus + other.bonus
        return Attribute(new_base, new_multiplier, new_bonus)

    def value(self):
        """
        value = base * multiplier + bonus
        multiplier can not be less than 10%
        """
        multiplier = max(10, self.multiplier)
        return int(self.base * multiplier / 100 + self.bonus)


