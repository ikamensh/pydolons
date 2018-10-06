from cmath import phase, pi


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def complex(self):
        return self.x + self.y * 1j

    @staticmethod
    def from_complex(c):
        return Cell( int(c.real + 0.5), int(c.imag+ 0.5)  )

    @staticmethod
    def maybe_complex(cell_or_complex):
        c_or_c = cell_or_complex
        return Cell(int(c_or_c.real), int(c_or_c.imag)) if isinstance(c_or_c, complex) else c_or_c

    @staticmethod
    def angle_between(c1, c2):
        """
        :param c1: complex vector 1
        :param c2: complex vector 2
        :return: smallest angle between the two vectors, and if it is ccw from c1 to c2
        """
        p1 = phase(c1)
        p2 = phase(c2)

        if p1 < 0 :
            p1 += 2 * pi

        if p2 < 0:
            p2 += 2 * pi

        angle = abs(p1 - p2)
        if angle > pi:
            angle = abs( angle - 2* pi )


        return  angle / pi * 180, p1 >= p2

    def __eq__(self, other):
        if self is other: return True
        if other is None: return False
        if self.__class__ != other.__class__: return False
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.x*10000 + self.y)

    def __repr__(self):
        return f"({self.x},{self.y})"
