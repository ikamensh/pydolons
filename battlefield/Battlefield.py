from math import hypot
from collections import namedtuple

Cell = namedtuple("Cell", "x y")

class Battlefield:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.units_at = {}
        self.unit_locations = {}

    @staticmethod
    def distance(p1, p2):
        return hypot(p1.x - p2.x, p1.y - p2.y)

    def get_units_dists_to(self, p, units_subset = None):
        unit_dist_tuples = [ (u, Battlefield.distance(p, self.unit_locations[u]))
                             for u in units_subset or self.unit_locations]
        return sorted(unit_dist_tuples, key=lambda x:x[1])

    def distance_unit_to_point(self, unit, p):
        assert unit in self.unit_locations
        unit_pos = self.unit_locations[unit]
        return Battlefield.distance(unit_pos, p)

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
                    if Battlefield.distance(cell, new_cell) <= distance:
                        neighbours.append(new_cell)

        return neighbours

    def get_nearest_cell(self, candidates, target):
        pairs = [(c, self.distance(c, target)) for c in candidates]
        return min(pairs, key=lambda x:x[1])



    def place(self, unit, p):

        assert 0 <= p.x < self.w
        assert 0 <= p.y < self.h
        assert p not in self.units_at

        self.units_at[p] = unit
        self.unit_locations[unit] = p

    def place_many(self, unit_locations):
        for char, p in unit_locations.items():
            self.place(char, p)


    def remove(self, unit):
        assert unit in self.unit_locations
        p = self.unit_locations[unit]
        del self.units_at[p]
        del self.unit_locations[unit]

    def move(self, unit, new_position):
        old_position = self.unit_locations[unit]
        self.remove(unit)
        self.place(unit, new_position)





