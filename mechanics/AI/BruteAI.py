from mechanics.AI import RandomAI
import random

class BruteAI:
    def __init__(self, game):
        self.game = game
        self.random_ai = RandomAI(game)

    def decide_step(self, active_unit, epsilon = 0.0) :

        if random.random() < epsilon:
            return self.random_ai.decide_step(active_unit)

        neighbour_nodes = self.game.get_all_neighbouring_states(active_unit)

        faction = self.game.factions[active_unit]
        # nodes_utils = [(node, node.utility(faction)) for node in neighbour_nodes] #easy debug
        best_node = max(neighbour_nodes, key= lambda x: x.utility(faction))

        return best_node.choice









