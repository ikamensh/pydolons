from math import hypot
from battlefield.Facing import Facing
from battlefield.Cell import Cell
from battlefield.Vision import Vision

class Battlefield:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.units_at = {}
        self.unit_locations = {}
        self.unit_facings = {}

    def x_sees_y(self, x, y):
        cells_x_sees = Vision.std_seen_cells(x, self)
        return self.unit_locations[y] in cells_x_sees

    @staticmethod
    def _distance(p1, p2):
        return hypot(p1.x - p2.x, p1.y - p2.y)

    def distance(self, one, another):
        if not isinstance(one, Cell):
            one = self.unit_locations[one]
        if not isinstance(another, Cell):
            another = self.unit_locations[another]
        return self._distance(one, another)

    def get_units_dists_to(self, p, units_subset = None):
        unit_dist_tuples = [ (u, self.distance(p, u))
                             for u in units_subset or self.unit_locations]
        return sorted(unit_dist_tuples, key=lambda x:x[1])

    def get_unit_at(self, cell):
        if cell in self.units_at:
            return self.units_at[cell]
        else:
            return None

    def get_neighbouring_cells(self, cell, distance=1):
        neighbours = self.get_cells_within_dist(cell, distance)
        neighbours.remove(cell)
        return neighbours

    def get_cells_within_dist(self, cell, distance):
        x = cell.x
        y = cell.y

        neighbours = []
        steps = list(range(-int(distance), int(distance) + 1))
        for dx in steps:
            for dy in steps:
                if 0 <= x + dx < self.w and 0 <= y + dy < self.h:
                    new_cell = Cell(x + dx, y + dy)
                    if self._distance(cell, new_cell) <= distance:
                        neighbours.append(new_cell)

        return neighbours

    def get_nearest_cell(self, candidates, target):
        pairs = [(c, self.distance(c, target)) for c in candidates]
        return min(pairs, key=lambda x:x[1])



    def place(self, unit, p, facing=None):

        assert 0 <= p.x < self.w
        assert 0 <= p.y < self.h
        assert p not in self.units_at

        self.units_at[p] = unit
        self.unit_locations[unit] = p
        self.unit_facings[unit] = facing or Facing.NORTH

    def place_many(self, unit_locations):
        for char, p in unit_locations.items():
            self.place(char, p)


    def remove(self, unit):
        assert unit in self.unit_locations
        p = self.unit_locations[unit]
        del self.units_at[p]
        del self.unit_locations[unit]

    def move(self, unit, new_position):
        self.remove(unit)
        self.place(unit, new_position)





