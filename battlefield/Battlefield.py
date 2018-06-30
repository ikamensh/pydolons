from math import hypot
from collections import namedtuple

Coordinates = namedtuple("Coordinates", "x y")

class Battlefield:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.units_at = {}
        self.unit_locations = {}

    @staticmethod
    def distance(p1, p2):
        return hypot(p1.x - p2.x, p1.y - p2.y)

    def get_units_dists_to(self, p):
        unit_dist_tuples = [ (u, Battlefield.distance(p, self.unit_locations[u]))
                             for u in self.unit_locations]
        return sorted(unit_dist_tuples, key=lambda x:x[1])

    def distance_unit_to_point(self, unit, p):
        assert unit in self.unit_locations
        unit_pos = self.unit_locations[unit]
        return Battlefield.distance(unit_pos, p)

    def place(self, unit, p):

        assert 0 <= p.x < self.w
        assert 0 <= p.y < self.h
        assert p not in self.units_at

        self.units_at[p] = unit
        self.unit_locations[unit] = p

    def place_many(self, units_and_their_locations):
        for char, p in units_and_their_locations:
            self.place(char, p)


    def remove(self, unit):
        assert unit in self.unit_locations
        p = self.unit_locations[unit]
        del self.units_at[p]
        del self.unit_locations[unit]

    def move(self, unit, new_p):
        self.remove(unit)
        self.place(unit, new_p)




