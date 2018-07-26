from mechanics.AI import RandomAI
import random

class BruteAI:
    def __init__(self, game):
        self.game = game
        self.random_ai = RandomAI(game)

    def decide_step(self, active_unit, epsilon = 0.0):

        if random.random() < epsilon:
            return self.random_ai.decide_step(active_unit)

        actions = self.game.get_all_choices(active_unit)
        choices = {}

        for a in actions:
            util = self.game.delta_util(*a)
            choices[util + random.random()] = a

        best_delta = max(choices.keys())
        print(choices.keys())
        print(best_delta)

        return choices[best_delta]









