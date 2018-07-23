from battlefield.Facing import FacingUtil
from battlefield.Cell import Cell
from math import hypot
import numpy as np
import functools

class Vision:

    def __init__(self, battlefield):
        self.battlefield = battlefield

    def std_seen_cells(self, unit):
        sight_range = unit.sight_range
        bf = self.battlefield
        facing = bf.unit_facings[unit]
        c_facing = FacingUtil.to_complex[facing]
        cell_from = bf.unit_locations[unit]

        v1 = (sight_range *2 /3 ) * 1j
        v2 = sight_range

        c1 = c_facing * v1 + FacingUtil.coord_to_complex(cell_from)
        c2 = c_facing * (v2-v1) + FacingUtil.coord_to_complex(cell_from)

        xmin, xmax = min(c1.real, c2.real), max(c1.real, c2.real)
        ymin, ymax = min(c1.imag, c2.imag), max(c1.imag, c2.imag)

        xmin, xmax, ymin, ymax = [int(x) for x in [xmin, xmax, ymin, ymax]]
        xmin = max(0, xmin)
        ymin = max(0, ymin)
        xmax = min(bf.w-1, xmax)
        ymax = min(bf.h-1, ymax)

        visible_cells = set()
        if c_facing.real:
            metric = Vision.dist_eliptic_y
        else:
            metric = Vision.dist_eliptic_x

        for x in range(xmin,xmax+1):
            for y in range(ymin, ymax+1):
                cell = Cell(x, y)
                if metric(cell_from, cell) <= sight_range:
                    visible_cells.add(cell)

        obstacles = {cell for cell in self.battlefield.units_at if cell in visible_cells}
        obstacles -= {cell_from}
        for obstacle in obstacles:
            for cell_to in set(visible_cells):
                if self.blocks(cell_from, cell_to, obstacle):
                    visible_cells.remove(cell_to)

        return visible_cells

    @staticmethod
    def dist_eliptic_x(p1, p2):
        return hypot( 1.45*(p1.x - p2.x) , (p1.y - p2.y) )

    @staticmethod
    def dist_eliptic_y(p1, p2):
        return hypot((p1.x - p2.x), 1.45*(p1.y - p2.y))

    @functools.lru_cache(maxsize=int(2**24))
    def blocks(self, looking_from, looking_to, obstacle):

        if looking_from.x > looking_to.x:
            return self.blocks(looking_to, looking_from, obstacle)

        if looking_to == obstacle:
            return False

        if looking_from == obstacle:
            return False

        if self.battlefield._distance(looking_from, looking_to) < self.battlefield._distance(looking_from, obstacle):
            return False


        norm = np.linalg.norm
        p1 = np.asarray([looking_from.x, looking_from.y])
        p2 = np.asarray([looking_to.x, looking_to.y])
        p3 = np.asarray([obstacle.x, obstacle.y])

        if np.dot( p2 - p1, p3 - p1) <= 0:
            return False


        dist_to_perpendicular = norm(np.cross(p2 - p1, p1 - p3)) / norm(p2 - p1)
        return dist_to_perpendicular < 0.65


