class SearchNode:
    def __init__(self, node_from, choice, game, fraction):
        self.node_from = node_from
        self.choice = choice
        self.game = game
        if game:
            self.utility = game.utility(fraction)
        else:
            self.utility = node_from.fake_measure(choice, fraction)

    def get_all_neighbouring_states(self, unit):
        if self.game is None:
            self.game = self.node_from.step_into_sim(*self.choice)
        return self.game.get_all_neighbouring_states(unit)

