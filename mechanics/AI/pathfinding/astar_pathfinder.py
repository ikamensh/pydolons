from __future__ import annotations
from astar import AStar
from collections import namedtuple
from battlefield import Battlefield
from mechanics.actives import ActiveTags
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_objects.battlefield_objects import Unit
    from typing import List, Tuple
    from mechanics.actives import Cost

Node = namedtuple("PathNode", "pos facing")


class StarSearch(AStar):

    def __init__(self, game, unit):
        super().__init__()
        self.game = game
        self.unit = unit
        self.w = game.bf.w
        self.h = game.bf.h
        self.costs_cache = {}

        self.transitions = self.build_transitions(unit)

    def neighbors(self, node):
        _neighbors = []
        for t in self.transitions:
            vector, rotation, cost = t
            pos, facing = node.pos + vector * node.facing, node.facing * rotation
            if 0 <= pos.real < self.w and 0 <= pos.imag < self.h:
                if self.game.bf.get_objects_at(pos) is not None:
                    continue
                new_node = Node(pos, facing)
                _neighbors.append(new_node)
                self.costs_cache[(node, new_node)] = cost
        return _neighbors

    def distance_between(self, n1, n2):
        cost = self.costs_cache[(n1, n2)]
        cost_factor = cost.stamina + cost.mana + cost.health + cost.readiness * 25
        return cost_factor / 5

    def heuristic_cost_estimate(self, current, goal):
        distance = abs(current.pos - goal.pos)
        return distance + abs(goal.facing - current.facing) / 10

    def is_goal_reached(self, current, goal):
        distance = abs(current.pos - goal.pos)
        return distance <= 1.5

    def path_to(self, _cell, desired_facing=1j):
        start = Node(self.unit.cell.complex, self.unit.facing)

        cell = _cell.complex if not isinstance(_cell, complex) else _cell
        end = Node(cell, desired_facing)

        path = self.astar(start, end)
        return list(path)

    @staticmethod
    def build_transitions(unit: Unit) -> List[Tuple[complex, complex, Cost]]:
        game = unit.game
        real_bf = game.bf

        bf = Battlefield(12, 12)
        game.battlefield = bf
        unit.cell = 5 + 5j

        choices = game.get_all_choices(unit)
        move_choices = [c for c in choices if ActiveTags.MOVEMENT in c[0].tags]

        game.battlefield = real_bf

        transitions = []
        for c in move_choices:
            action, cell = c
            vector = cell.complex - unit.cell.complex
            rotation = 1 + 0j
            transitions.append((vector, rotation, action.cost))

        transitions.append((0j, -1j, unit.turn_cw_active.cost))
        transitions.append((0j, 1j, unit.turn_ccw_active.cost))

        return transitions
