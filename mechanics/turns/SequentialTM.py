from mechanics.turns import TurnsManager
from collections import deque


class SequentialTM(TurnsManager):
    def __init__(self, units=None):
        self.units = deque(units or [])

    def get_next(self):
        unit = self.units[-1]
        self.units.rotate(1)
        return unit

    def add_unit(self, unit):
        self.units.appendleft(unit)

    def remove_unit(self, unit):
        assert unit in self.units
        self.units.remove(unit)
