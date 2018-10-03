from mechanics.AI import RandomAI
import random

class BroadAI:
    def __init__(self, game):
        self.game = game
        self.random_ai = RandomAI(game)

    def decide_step(self, active_unit, epsilon = 0.0):

        if random.random() < epsilon:
            return self.random_ai.decide_step(active_unit)

        circle1 = self.game.get_all_neighbouring_states(active_unit)

        circle2 = []
        for node in circle1:
            circle2 += node.get_all_neighbouring_states(active_unit)

        fraction = self.game.fractions[active_unit]
        utilities = {node:(node.utility(fraction) + node.node_from.utility(fraction)) for node in circle2}
        # this bug a lot of taps
        best_node2 = max(circle2, key=lambda x: utilities[x])
        best_node1 = best_node2.node_from

        return best_node1.choice
