from mechanics.fractions import Fractions
from mechanics.AI import RandomAI
from astar import AStar
from mechanics.damage import Damage

class StarPathSearch(AStar):
    really_big_number = 1e50

    def __init__(self, battlefield):
        super().__init__()
        self.battlefield = battlefield
        self.unit = None

    def neighbors(self, node):
        return self.battlefield.get_neighbouring_cells(node)

    def distance_between(self, n1, n2):
        assert self.unit is not None
        if n2 in self.battlefield.units_at:
            obstacle = self.battlefield.units_at[n2]
            damage_per_turn = Damage.calculate_damage(self.unit.get_melee_weapon().damage, obstacle)[0]
            if damage_per_turn == 0:
                return StarPathSearch.really_big_number
            n_turns = obstacle.health / damage_per_turn
            return n_turns + 1
        else:
            return 1

    def heuristic_cost_estimate(self, current, goal):
        return self.battlefield.distance(current, goal)





class AstarAI:
    def __init__(self, game):
        self.game = game
        self.battlefield = game.battlefield
        self.fractions = game.fractions
        self.random_ai = RandomAI(game)
        self.astar = StarPathSearch(game)

    def decide_step(self, active_unit, target_fraction=Fractions.PLAYER):
        # assert active_unit in self.battlefield.unit_locations
        assert active_unit in self.battlefield

        start_location = self.battlefield.unit_locations[active_unit]

        target_units = [unit for unit, fraction in self.fractions.items() if fraction is target_fraction]

        if target_units:
            distances = self.battlefield.get_units_dists_to(start_location, units_subset=target_units)
            target, _ = distances[0]
            target_location = self.battlefield.unit_locations[target]

            self.astar.unit = active_unit
            path = self.astar.astar(start_location, target_location)
            if path is None:
                return self.random_ai.decide_step(active_unit)

            return list(path)[1]

        else:
            return self.random_ai.decide_step(active_unit)

