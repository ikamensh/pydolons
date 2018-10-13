from battlefield.Facing import Facing
from battlefield.Cell import Cell
from battlefield.Vision import Vision
import game_objects.battlefield_objects as bf_objs
import typing

class Battlefield:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.units_at = {}              #cell -> unit
        self.unit_locations: typing.Dict[bf_objs.BattlefieldObject:Cell] = {}        #unit -> cell
        self.unit_facings :typing.Dict[bf_objs.Unit:complex] = {}          #unit -> direction
        self.vision = Vision(self)

    def x_sees_y(self, x, y):
        if x.is_obstacle:
            return False

        cells_x_sees = self.vision.std_seen_cells(x)
        return self.unit_locations[y] in cells_x_sees


    def distance(self, one, another):
        if isinstance(one, bf_objs.BattlefieldObject):
            one = self.unit_locations[one]
        if isinstance(another, bf_objs.BattlefieldObject):
            another = self.unit_locations[another]
        return Cell._distance(Cell.maybe_complex(one), Cell.maybe_complex(another))

    def get_units_dists_to(self, p, units_subset = None):
        unit_dist_tuples = [ (u, self.distance(p, u))
                             for u in units_subset or self.unit_locations]
        return sorted(unit_dist_tuples, key=lambda x:x[1])

    def get_units_within_radius(self, center, radius):
        return [ u for u in self.unit_locations if self.distance(center, u) <= radius]

    def get_unit_at(self, _cell):
        cell = Cell.maybe_complex(_cell)
        if cell in self.units_at:
            return self.units_at[cell]
        else:
            return None

    def neighbours_exclude_center(self, cell, distance=1):
        neighbours = set(self.get_cells_within_dist(cell, distance))
        neighbours.remove(cell)
        return neighbours

    def get_cells_within_dist(self, cell, distance):
        return Cell.get_neighbours(cell,distance, self.w, self.h)

    def get_nearest_cell(self, candidates, target):
        pairs = [(c, self.distance(c, target)) for c in candidates]
        return min(pairs, key=lambda x:x[1])



    def place(self, unit, _p, facing=None):
        import game_objects.battlefield_objects as bf_objs

        p = Cell.maybe_complex(_p)

        assert 0 <= p.x < self.w
        assert 0 <= p.y < self.h
        assert p not in self.units_at

        self.units_at[p] = unit
        self.unit_locations[unit] = p
        if isinstance(unit, bf_objs.Unit):
            self.unit_facings[unit] = facing or Facing.NORTH

    def remove(self, unit):
        assert unit in self.unit_locations
        p = self.unit_locations[unit]
        del self.units_at[p]
        del self.unit_locations[unit]
        if not unit.is_obstacle:
            del self.unit_facings[unit]

    def move(self, unit, new_position):
        unit_facing = self.unit_facings[unit]
        self.remove(unit)
        self.place(unit, new_position, unit_facing)


    def angle_to(self, unit, target):
        target_cell = target if isinstance(target, Cell) else self.unit_locations[target]
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
        result = set()
        for i in range(self.w):
            for j in range(self.h):
                result.add(Cell(i, j))
        return result


    def units_in_area(self, cells : typing.Collection[Cell]):
        cells_with_units = set(self.units_at.keys()).intersection(set(cells))
        return [self.units_at[c] for c in cells_with_units]


    def __iter__(self):
        for unit in self.unit_locations:
            if not unit.is_obstacle:
                yield unit
