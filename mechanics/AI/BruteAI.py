from mechanics.fractions import Fractions
from mechanics.AI import RandomAI

class BruteAI:
    def __init__(self, battlefield, fractions):
        self.battlefield = battlefield
        self.fractions = fractions
        self.random_ai = RandomAI(battlefield)

    def decide_step(self, active_unit, target_fraction=Fractions.PLAYER):
        assert active_unit in self.battlefield.unit_locations

        start_location = self.battlefield.unit_locations[active_unit]

        target_units = [unit for unit, fraction in self.fractions.items() if fraction is target_fraction]

        if target_units:
            distances = self.battlefield.get_units_dists_to(start_location)
            target = distances[0]
            target_location = self.battlefield.unit_locations[target]
            possible_steps = self.battlefield.get_neighbouring_cells(start_location)
            return self.battlefield.get_nearest_to(candidates=possible_steps, target=target_location)

        else:
            return self.random_ai.decide_step(active_unit)

