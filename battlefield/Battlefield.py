from battlefield.Facing import Facing
from battlefield.Cell import Cell
from battlefield.Vision import Vision
import game_objects.battlefield_objects as bf_objs

class Battlefield:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.units_at = {}              #cell -> unit
        self.unit_locations = {}        #unit -> cell
        self.unit_facings = {}          #unit -> direction
        self.vision = Vision(self)

    def x_sees_y(self, x, y):
        if x.is_obstacle:
            return False

        cells_x_sees = self.vision.std_seen_cells(x)
        return self.unit_locations[y] in cells_x_sees

    @staticmethod
    def _distance(p1, p2):
        return Vision._distance(p1, p2)

    def distance(self, one, another):
        if isinstance(one, bf_objs.BattlefieldObject):
            one = self.unit_locations[one]
        if isinstance(another, bf_objs.BattlefieldObject):
            another = self.unit_locations[another]
        return self._distance(Cell.maybe_complex(one), Cell.maybe_complex(another))

    def get_units_dists_to(self, p, units_subset = None):
        unit_dist_tuples = [ (u, self.distance(p, u))
                             for u in units_subset or self.unit_locations]
        return sorted(unit_dist_tuples, key=lambda x:x[1])

    def get_unit_at(self, _cell):
        cell = Cell.maybe_complex(_cell)
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



    def place(self, unit, _p, facing=None):
        p = Cell.maybe_complex(_p)

        assert 0 <= p.x < self.w
        assert 0 <= p.y < self.h
        assert p not in self.units_at

        self.units_at[p] = unit
        self.unit_locations[unit] = p
        if isinstance(unit, bf_objs.Unit):
            self.unit_facings[unit] = facing or Facing.NORTH

    def place_many(self, unit_locations):
        for char, p in unit_locations.items():
            self.place(char, p)


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

    @property
    def all_cells(self):
        result = set()
        for i in range(self.w):
            for j in range(self.h):
                result.add(Cell(i,j))
        return result

    def __iter__(self):
        for unit in self.unit_locations:
            if not unit.is_obstacle:
                yield unit





