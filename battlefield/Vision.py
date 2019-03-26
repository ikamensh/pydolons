from __future__ import annotations
from battlefield import Cell, Battlefield
import numpy as np
import functools
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_objects.battlefield_objects import Unit
    from DreamGame import DreamGame


class Vision:
    def __init__(self, game: DreamGame):
        self.game = game

    def x_sees_y(self, x, y):
        if x.is_obstacle:
            return False

        cells_x_sees = self.std_seen_cells(x)
        return y.cell in cells_x_sees

    def std_seen_cells(self, unit: Unit):
        bf = self.game.bf

        cell_from = unit.cell
        visible_cells = set(self._std_vision_field(unit.sight_range,
                                                   unit.facing,
                                                   cell_from,
                                                   self.game.bf))
        blocking_cells = {cell for cell in bf.cells_to_objs if bf.space_free(cell) <
                          bf.space_per_cell / 2}
        blocking_cells -= {cell_from}
        visible_walls = frozenset({cell for cell in bf.walls if cell in visible_cells})
        diag_wall_blockers = Vision._merge_walls(visible_walls)
        blocking_cells |= diag_wall_blockers
        for obstacle in blocking_cells:
            for cell_to in set(visible_cells):
                if Vision.blocks(cell_from, cell_to, obstacle):
                    visible_cells.remove(cell_to)

        return visible_cells

    @staticmethod
    @functools.lru_cache(maxsize=int(2**8))
    def _merge_walls(obstacles):
        """
        Creates new artificial obstacles to enable diagonal walls.
        :param obstacles: all obstacles within sight
        :return: set of new imaginary obstacles
        """
        new_obstacles = set()
        diag_dist = Cell._distance(Cell(0,0), Cell(1,1))
        for o1 in obstacles:
            for o2 in obstacles:
                if Cell._distance(o1, o2) == diag_dist:
                    new_obstacles.add(Cell( (o1.x+o2.x)/2 , (o1.y+o2.y)/2 ))

        return new_obstacles

    @staticmethod
    @functools.lru_cache(maxsize=int(2**10))
    def _std_vision_field(sight_range, facing, cell_from, bf):
        """
        :return: a set of cells from battlefield :bf which are normally visible
        from :cell_from when facing in the direction :facing and having :sight_range
        """
        w = bf.h
        h = bf.h

        v1 = (sight_range * 2 / 3 + 1) * 1j
        v2 = sight_range

        c1 = facing * v1 + cell_from.complex
        c2 = facing * (v2 - v1) + cell_from.complex

        # max vision box - rough approximation, strictly bigger area
        xmin, xmax = min(c1.real, c2.real), max(c1.real, c2.real)
        ymin, ymax = min(c1.imag, c2.imag), max(c1.imag, c2.imag)

        xmin, xmax, ymin, ymax = [int(x) for x in [xmin, xmax, ymin, ymax]]
        xmin = max(0, xmin)
        ymin = max(0, ymin)
        xmax = min(w - 1, xmax)
        ymax = min(h - 1, ymax)

        visible_cells = set()
        if facing.real:
            metric = Vision._dist_eliptic_y
        else:
            metric = Vision._dist_eliptic_x

        for x in range(xmin, xmax + 1):
            for y in range(ymin, ymax + 1):
                cell = Cell(x, y)
                if metric(cell_from, cell) <= sight_range:
                    visible_cells.add(cell)

        return frozenset(visible_cells)

    @staticmethod
    def _dist_eliptic_x(p1, p2):
        return Cell._hypot( 1.45*(p1.x - p2.x) , (p1.y - p2.y) )

    @staticmethod
    def _dist_eliptic_y(p1, p2):
        return Cell._hypot((p1.x - p2.x), 1.45*(p1.y - p2.y))


    @staticmethod
    @functools.lru_cache(maxsize=int(2**16))
    def blocks(looking_from: Cell, looking_to: Cell, obstacle: Cell)-> bool:
        """
        tests if the cell :obstacle is blocking
        when :looking_from towards :looking_to
        :return: True if the :obstacle blocks the view
        """

        # caching trick: halve the search space (assumes symmetry, which is tested)
        if looking_from.x > looking_to.x:
            return Vision.blocks(looking_to, looking_from, obstacle)

        if looking_to == obstacle:
            return False

        if looking_from == obstacle:
            return False

        #obstacle behind the target can't block it.
        if Cell._distance(looking_from, looking_to) < Cell._distance(looking_from, obstacle):
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


