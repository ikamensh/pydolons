from mechanics.fractions import Fractions
from battlefield.Battlefield import Cell
from utils.numeric import clamp
import random

class RandomAI:
    def __init__(self, battlefield):
        self.battlefield = battlefield


    def decide_step(self, active_unit):
        assert active_unit in self.battlefield.unit_locations

        location = self.battlefield.unit_locations[active_unit]

        step = [-1, 0, 1]

        x_new = clamp(location.x + random.choice(step), 0, self.battlefield.w)
        y_new = clamp(location.y + random.choice(step), 0, self.battlefield.h)
        return Cell(x_new, y_new)

