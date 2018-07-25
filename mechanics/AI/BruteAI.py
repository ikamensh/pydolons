from mechanics.fractions import Fractions
from mechanics.AI import RandomAI
import random

class BruteAI:
    def __init__(self, game):
        self.game = game
        self.random_ai = RandomAI(game)

    def decide_step(self, active_unit, epsilon = 0.1):

        if random.random() < epsilon:
            return self.random_ai.decide_step(active_unit)

        fraction = self.game.fractions[active_unit]


        actives = active_unit.actives

        targets = {}
        for a in actives:
            if a.owner_can_afford_activation():
                tgts = self.game.get_possible_targets(a)
                if tgts:
                    targets[a] = tgts

        actives_with_valid_targets = set(targets.keys())
        actives_without_targeting = {a for a in actives if a.targeting_cls is None}

        choices = {}

        for active in actives_without_targeting:
            util = self.game.delta_util(active, None)
            choices[util] = (active, None)

        for active in actives_with_valid_targets:
            for target in targets[active]:
                choices[self.game.delta_util(active, target)] = (active, target)

        best_delta = max(choices.keys())

        return choices[best_delta]









