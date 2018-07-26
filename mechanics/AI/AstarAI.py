from mechanics.fractions import Fractions
from mechanics.AI import RandomAI, SearchNode
from astar import AStar

class StarSearch(AStar):
    really_big_number = 1e50

    def __init__(self, game, unit):
        super().__init__()
        self.game = game
        self.unit = unit
        self.fraction = self.game.fractions[self.unit]
        self.visited = []

    def neighbors(self, node):

        neighbours = node.get_all_neighbouring_states(self.unit)
        self.visited += neighbours
        return neighbours

    def distance_between(self, n1, n2):
        return n1.utility(self.fraction) - n2.utility(self.fraction)

    def heuristic_cost_estimate(self, current, goal):
        return -current.utility(self.fraction)

    def is_goal_reached(self, current, goal):
        return len(self.visited) >= 100


class AstarAI:
    def __init__(self, game):
        self.game = game
        self.random_ai = RandomAI(game)


    def decide_step(self, active_unit):

        astar = StarSearch(self.game, active_unit)
        path = astar.astar(SearchNode(None, None, self.game), None)
        node = list(path)[1]
        action = node.action
        return action

