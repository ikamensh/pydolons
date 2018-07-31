class SearchNode:
    def __init__(self, node_from, choice, game):
        self.node_from = node_from
        self.choice = choice
        self.game = game

    def utility(self, fraction):
        if self.game:
            return self.game.utility(fraction)
        else:
            return self.node_from.game.fake_measure(self.choice, fraction)

    def get_all_neighbouring_states(self, unit):
        if self.game is None:
            self.game = self.node_from.game.step_into_sim(*self.choice)
        nodes = self.game.get_all_neighbouring_states(unit)
        for node in nodes:
            node.node_from = self

        return nodes

    def __repr__(self):
        return f"{len(self.game.units) if self.game else 'Lazy'} via {self.choice[0]} targeted on {self.choice[1]}"

