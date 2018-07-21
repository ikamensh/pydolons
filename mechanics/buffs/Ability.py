import copy

class Ability:
    def __init__(self, bonuses = None):
        self.bonuses = bonuses
        self.bound_to = None

    def apply_to(self, unit):
        cpy = copy.deepcopy(self)
        unit.abilities.append(cpy)
        cpy.bound_to = unit

    def deactivate(self):
        self.bound_to.abilities.remove(self)
        self.bound_to = None


