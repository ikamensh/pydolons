from mechanics.AI import RandomAI
import random

class BruteAI:
    def __init__(self, game):
        self.game = game
        self.random_ai = RandomAI(game)

    def decide_step(self, active_unit, epsilon = 0.1):

        if random.random() < epsilon:
            return self.random_ai.decide_step(active_unit)

        actions = self.game.get_all_actions(active_unit)
        choices = {}

        for a in actions:
            util = self.game.delta_util(*a)
            choices[util] = a

        best_delta = max(choices.keys())

        return choices[best_delta]









