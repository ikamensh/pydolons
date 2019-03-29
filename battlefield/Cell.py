from __future__ import annotations
from cmath import phase, pi
import functools
from math import hypot
from typing import Union, List, Tuple


def positive_angle(angle):
    assert -pi * 2 <= angle < 2 * pi
    if angle < 0:
        return angle + 2 * pi
    else:
        return angle


def cw_phase(c):
    p = phase(c)
    return positive_angle(p)


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def complex(self) -> complex:
        return self.x + self.y * 1j

    @staticmethod
    def from_complex(c: complex) -> Cell:
        return Cell(int(c.real + 0.5), int(c.imag + 0.5))

    @staticmethod
    def maybe_complex(cell_or_complex: Union[Cell, complex]) -> Cell:
        c_or_c = cell_or_complex
        return Cell(int(c_or_c.real), int(c_or_c.imag)
                    ) if isinstance(c_or_c, complex) else c_or_c

    @staticmethod
    def angle_between(c1: complex, c2: complex) -> Tuple[float, bool]:
        """
        :return: smallest angle between the two vectors, and if it is ccw from c1 to c2
        """
        if c1 == 0j or c2 == 0j or c1 == -0j or c2 == -0j:
            return 0, True

        p1 = cw_phase(c1)
        p2 = cw_phase(c2)

        angle_cw = positive_angle(p2 - p1)
        angle_ccw = positive_angle(p1 - p2)

        return min(angle_cw, angle_ccw) / pi * 180, angle_ccw < angle_cw

    @staticmethod
    @functools.lru_cache()
    def get_neighbours(
            cell_or_complex,
            distance,
            w=1000,
            h=1000) -> List[Cell]:
        c = Cell.maybe_complex(cell_or_complex)

        neighbours = []
        x_min, x_max = int(max(0, c.x - distance)
                           ), int(min(w - 1, c.x + distance))
        y_min, y_max = int(max(0, c.y - distance)
                           ), int(min(h - 1, c.y + distance))

        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                test_cell = Cell(x, y)
                if Cell._distance(c, test_cell) <= distance:
                    neighbours.append(test_cell)

        return neighbours

    @staticmethod
    def _distance(p1, p2):
        return Cell._hypot(p1.x - p2.x, p1.y - p2.y)

    @staticmethod
    @functools.lru_cache(maxsize=2**9)
    def _hypot(x, y):
        return hypot(x, y)

    def __eq__(self, other):
        if self is other:
            return True
        if other is None:
            return False
        if isinstance(other, complex):
            return self.x == other.real and self.y == other.imag
        if self.__class__ != other.__class__:
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.x * 10000 + self.y)

    def __repr__(self):
        return f"({self.x},{self.y})"
