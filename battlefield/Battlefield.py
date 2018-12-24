from __future__ import annotations
from typing import Dict, Collection, List, TYPE_CHECKING
if TYPE_CHECKING:
    from game_objects.battlefield_objects import Unit, BattlefieldObject, Obstacle

from battlefield.Facing import Facing
from battlefield.Cell import Cell
from battlefield.Vision import Vision
from my_utils.utils import flatten



class Battlefield:

    space_per_cell = 10
    space_per_unit = 3
    space_per_obstacle = 10

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.unit_locations: Dict[BattlefieldObject,Cell] = {}
        self.unit_facings :Dict[Unit, complex] = {}
        self.vision = Vision(self)

    def x_sees_y(self, x, y):
        if x.is_obstacle:
            return False

        cells_x_sees = self.vision.std_seen_cells(x)
        return self.unit_locations[y] in cells_x_sees


    def distance(self, one, another):
        if hasattr(one, "alive"):
            one = self.unit_locations[one]
        if hasattr(another, "alive"):
            another = self.unit_locations[another]
        return Cell._distance(Cell.maybe_complex(one), Cell.maybe_complex(another))

    def get_units_dists_to(self, p, units_subset = None):
        unit_dist_tuples = [ (u, self.distance(p, u))
                             for u in units_subset or self.unit_locations]
        return sorted(unit_dist_tuples, key=lambda x:x[1])

    def get_units_within_radius(self, center, radius):
        return [ u for u in self.unit_locations if self.distance(center, u) <= radius]

    def get_units_at(self, _cell):
        cell = Cell.maybe_complex(_cell)
        if cell in self.units_at:
            return self.units_at[cell]
        else:
            return None



    def neighbours_exclude_center(self, cell, distance=1) -> List[Cell]:
        neighbours = set(self.get_cells_within_dist(cell, distance))
        neighbours.remove(cell)
        return list(neighbours)

    def get_cells_within_dist(self, cell, distance) -> List[Cell]:
        return Cell.get_neighbours(cell,distance, self.w, self.h)

    def get_nearest_cell(self, candidates, target):
        pairs = [(c, self.distance(c, target)) for c in candidates]
        return min(pairs, key=lambda x:x[1])



    def place(self, unit, _p, facing=None):
        p = Cell.maybe_complex(_p)

        assert 0 <= p.x < self.w
        assert 0 <= p.y < self.h

        self.unit_locations[unit] = p
        if not unit.is_obstacle:
            self.unit_facings[unit] = facing or Facing.NORTH

    def remove(self, unit):
        assert unit in self.unit_locations
        del self.unit_locations[unit]
        if not unit.is_obstacle:
            del self.unit_facings[unit]

    def move(self, unit, new_position):
        self.unit_locations[unit] = Cell.maybe_complex(new_position)


    def space_free(self, cell):
        units = self.get_units_at(cell)
        if not units:
            return self.space_per_cell
        space_taken = sum([self.space_per_obstacle for u in units if u.is_obstacle] +
                          [self.space_per_unit for u in units if not u.is_obstacle])
        return self.space_per_cell - space_taken


    def angle_to(self, unit, target):
        if isinstance(target, complex):
            target_cell = Cell.from_complex(target)
        elif isinstance(target, Cell):
            target_cell = target
        else:
            target_cell = self.unit_locations[target]

        facing = self.unit_facings[unit]
        location = self.unit_locations[unit]
        vector_to_target = target_cell.complex - location.complex
        if vector_to_target == 0j:
            return 9000, None
        return Cell.angle_between(facing, vector_to_target)

    @staticmethod
    def _distance(p1, p2):
        return Cell._distance(p1, p2)

    @property
    def all_cells(self):
        if hasattr(self, "_all_cells"):
            return self._all_cells

        result = set()
        for i in range(self.w):
            for j in range(self.h):
                result.add(Cell(i, j))

        self._all_cells = result
        return result

    @property
    def all_units(self) -> List[Unit]:
        return [u for u in self.unit_locations.keys() if not u.is_obstacle] # avoiding direct import

    @property
    def all_obstacles(self) -> List[Obstacle]:
        return [u for u in self.unit_locations.keys() if u.is_obstacle] # avoiding direct import


    def units_in_area(self, cells : Collection[Cell]) -> List[Unit]:
        cells_with_units = set(self.units_at.keys()).intersection(set(cells))
        return list(flatten(self.units_at[c] for c in cells_with_units))

    #optimize: use dirty bit
    @property
    def units_at(self) -> Dict[Cell, List[BattlefieldObject]]:
        result = {}
        for unit, cell in self.unit_locations.items():
            if cell not in result:
                result[cell] = [unit]
            else:
                result[cell].append(unit)

        return result

    def cone(self, cell_from, direction, angle_max, dist_min, dist_max):
        result = []
        for cell in self.all_cells:
            if dist_min <= self.distance(cell, cell_from) <= dist_max:
                vector_to_target = cell.complex - cell_from.complex
                if Cell.angle_between(direction, vector_to_target)[0] <= angle_max:
                    result.append(cell)

        return result


    def __iter__(self):
        for unit in self.unit_locations:
            if not unit.is_obstacle:
                yield unit
