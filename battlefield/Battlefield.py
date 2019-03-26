from __future__ import annotations
from typing import Dict, Collection, List, TYPE_CHECKING
if TYPE_CHECKING:
    from game_objects.battlefield_objects import BattlefieldObject, Wall
    from typing import Set, FrozenSet, Collection
    import DreamGame
from battlefield.Cell import Cell
from collections import defaultdict
from my_utils.utils import ReadOnlyDict

class Battlefield:

    space_per_cell = 10

    def __init__(self, w, h, game: DreamGame = None, walls: Collection[Wall] = frozenset()):
        self.w = w
        self.h = h
        self.game = game
        self._walls = frozenset(walls)
        self.walls = ReadOnlyDict({w.cell:w for w in self._walls})

        all_cells = []
        for i in range(self.w):
            for j in range(self.h):
                all_cells.append(Cell(i, j))
        self.all_cells = frozenset(all_cells)

    def set_new_walls(self, new_walls: Collection[Wall]):
        self._walls = frozenset(new_walls)
        self.walls = ReadOnlyDict({w.cell: w for w in self._walls})

    @property
    def all_objs(self):
        return self.game.units | self.game.obstacles

    @staticmethod
    def distance(one, another):
        if hasattr(one, "alive"):
            one = one.cell
        if hasattr(another, "alive"):
            another = another.cell
        return Cell._distance(Cell.maybe_complex(one), Cell.maybe_complex(another))

    @staticmethod
    def get_units_dists_to(p, units_subset):
        unit_dist_tuples = [ (u, Battlefield.distance(p, u)) for u in units_subset]
        return sorted(unit_dist_tuples, key=lambda x:x[1])

    def get_units_within_radius(self, center, radius):
        return [u for u in self.all_objs if Battlefield.distance(center, u) <= radius]

    def get_objects_at(self, _cell) -> List[BattlefieldObject]:
        cell = Cell.maybe_complex(_cell)
        if cell in self.cells_to_objs:
            return self.cells_to_objs[cell]


    def neighbours_exclude_center(self, cell, distance=1) -> List[Cell]:
        neighbours = set(self.get_cells_within_dist(cell, distance))
        neighbours.remove(cell)
        return list(neighbours)

    def get_cells_within_dist(self, cell, distance) -> List[Cell]:
        return Cell.get_neighbours(cell,distance, self.w, self.h)

    def get_nearest_cell(self, candidates, target):
        pairs = [(c, self.distance(c, target)) for c in candidates]
        return min(pairs, key=lambda x:x[1])

    def space_free(self, cell: Cell):
        space_taken = sum([o.size for o in self.get_objects_at(cell)])
        return self.space_per_cell - space_taken

    @staticmethod
    def angle_to(unit, target):
        if isinstance(target, complex):
            target_cell = Cell.from_complex(target)
        elif isinstance(target, Cell):
            target_cell = target
        else:
            target_cell = target.cell

        vector_to_target = target_cell.complex - unit.cell.complex
        if vector_to_target == 0j:
            return 9000, None
        return Cell.angle_between(unit.facing, vector_to_target)


    @property
    def cells_to_objs(self) -> Dict[Cell, List[BattlefieldObject]]:
        result = defaultdict(list)
        for unit in self.all_objs:
            result[unit.cell].append(unit)
        return result


    def units_in_area(self, area : Collection[Cell]) -> List[BattlefieldObject]:
        return [u for u in self.all_objs if u.cell in area]

    def cone(self, cell_from, direction:complex, angle_max, dist_min, dist_max):
        result = []
        for cell in self.all_cells:
            if dist_min <= self.distance(cell, cell_from) <= dist_max:
                vector_to_target = cell.complex - cell_from.complex
                if Cell.angle_between(direction, vector_to_target)[0] <= angle_max:
                    result.append(cell)

        return result


    @staticmethod
    def _distance(p1, p2):
        return Cell._distance(p1, p2)

