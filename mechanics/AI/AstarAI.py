from mechanics.AI import RandomAI, SearchNode
from astar import AStar

class StarSearch(AStar):
    really_big_number = 1e50

    def __init__(self, game, unit, depth_limit):
        super().__init__()
        self.game = game
        self.unit = unit
        self.fraction = self.game.fractions[self.unit]
        self.visited = []
        self.depth_limit = depth_limit

    def neighbors(self, node):
        neighbours = node.get_all_neighbouring_states(self.unit)
        self.visited += neighbours
        return neighbours

    def distance_between(self, n1, n2):
        #TODO maybe we need to ensure actual measurement on the nodes, not the fast, emulated one.
        return n1.utility(self.fraction) - n2.utility(self.fraction)

    def heuristic_cost_estimate(self, current, goal):
        return -current.utility(self.fraction)

    def is_goal_reached(self, current, goal):
        return len(self.visited) >= self.depth_limit


class AstarAI:
    def __init__(self, game):
        self.game = game
        self.random_ai = RandomAI(game)


    def decide_step(self, active_unit, depth_limit=50):

        astar = StarSearch(self.game, active_unit, depth_limit)
        start = SearchNode(None, None, self.game)
        path = astar.astar(start, None)
        node = list(path)[1]
        choice = node.choice
        return choice

