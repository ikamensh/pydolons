from battlefield.Facing import FacingUtil
from battlefield.Cell import Cell
from math import hypot
import numpy as np
import functools

class Vision:

    def __init__(self, battlefield):
        self.battlefield = battlefield

    def std_seen_cells(self, unit):
        bf = self.battlefield
        facing = bf.unit_facings[unit]

        cell_from = bf.unit_locations[unit]
        visible_cells = self.std_vision_field(unit.sight_range, facing, cell_from, bf)
        obstacles = {cell for cell in self.battlefield.units_at if cell in visible_cells}
        obstacles -= {cell_from}
        walls = frozenset({cell for cell in self.battlefield.units_at if cell in visible_cells and
                 self.battlefield.units_at[cell].is_obstacle})
        diag_wall_blockers = self.merge_walls(walls)
        obstacles |= diag_wall_blockers
        for obstacle in obstacles:
            for cell_to in set(visible_cells):
                if self.blocks(cell_from, cell_to, obstacle):
                    visible_cells.remove(cell_to)

        return visible_cells

    @staticmethod
    @functools.lru_cache(maxsize=int(2**8))
    def merge_walls(obstacles):
        """
        Creates new artificial obstacles to enable diagonal walls.
        :param obstacles: all obstacles within sight
        :return: set of new imaginary obstacles
        """
        new_obstacles = set()
        diag_dist = Vision._distance(Cell(0,0), Cell(1,1))
        for o1 in obstacles:
            for o2 in obstacles:
                if Vision._distance(o1, o2) == diag_dist:
                    new_obstacles.add(Cell( (o1.x+o2.x)/2 , (o1.y+o2.y)/2 ))

        return new_obstacles




    @staticmethod
    @functools.lru_cache(maxsize=int(2**10))
    def std_vision_field(sight_range, facing, cell_from, bf):
        w = bf.h
        h = bf.h
        c_facing = FacingUtil.to_complex[facing]
        v1 = (sight_range * 2 / 3) * 1j
        v2 = sight_range

        c1 = c_facing * v1 + FacingUtil.coord_to_complex(cell_from)
        c2 = c_facing * (v2 - v1) + FacingUtil.coord_to_complex(cell_from)

        xmin, xmax = min(c1.real, c2.real), max(c1.real, c2.real)
        ymin, ymax = min(c1.imag, c2.imag), max(c1.imag, c2.imag)

        xmin, xmax, ymin, ymax = [int(x) for x in [xmin, xmax, ymin, ymax]]
        xmin = max(0, xmin)
        ymin = max(0, ymin)
        xmax = min(w - 1, xmax)
        ymax = min(h - 1, ymax)

        visible_cells = set()
        if c_facing.real:
            metric = Vision.dist_eliptic_y
        else:
            metric = Vision.dist_eliptic_x

        for x in range(xmin, xmax + 1):
            for y in range(ymin, ymax + 1):
                cell = Cell(x, y)
                if metric(cell_from, cell) <= sight_range:
                    visible_cells.add(cell)

        return visible_cells

    @staticmethod
    def dist_eliptic_x(p1, p2):
        return hypot( 1.45*(p1.x - p2.x) , (p1.y - p2.y) )

    @staticmethod
    def dist_eliptic_y(p1, p2):
        return hypot((p1.x - p2.x), 1.45*(p1.y - p2.y))

    @staticmethod
    def _distance(p1, p2):
        return Vision.__hypot(p1.x - p2.x, p1.y - p2.y)

    @staticmethod
    @functools.lru_cache()
    def __hypot(x, y):
        return hypot(x, y)

    @staticmethod
    @functools.lru_cache(maxsize=int(2**16))
    def blocks(looking_from, looking_to, obstacle):

        # caching trick: halve the search space (assumes symmetry, which is tested)
        if looking_from.x > looking_to.x:
            return Vision.blocks(looking_to, looking_from, obstacle)

        if looking_to == obstacle:
            return False

        if looking_from == obstacle:
            return False

        #obstacle behind the target can't block it.
        if Vision._distance(looking_from, looking_to) < Vision._distance(looking_from, obstacle):
            return False


        norm = np.linalg.norm
        p1 = np.asarray([looking_from.x, looking_from.y])
        p2 = np.asarray([looking_to.x, looking_to.y])
        p3 = np.asarray([obstacle.x, obstacle.y])

        #obstacle which is in diferent semiplane can't possibly block it
        if np.dot( p2 - p1, p3 - p1) <= 0:
            return False


        dist_to_perpendicular = norm(np.cross(p2 - p1, p1 - p3)) / norm(p2 - p1)
        return dist_to_perpendicular < 0.65


