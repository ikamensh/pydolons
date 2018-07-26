class SearchNode:
    def __init__(self, node_from, action, game):
        self.node_from = node_from
        self.action = action
        self.game = game

    def get_all_neighbouring_states(self, unit):
        return self.game.get_all_neighbouring_states(unit)

    def utility(self, fraction):
        return self.game.utility(fraction)