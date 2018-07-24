from cmath import phase, pi

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def complex(self):
        return self.x + self.y * 1j

    @staticmethod
    def angle_between(c1, c2):
        p1 = phase(c1)
        p2 = phase(c2)

        if p1 < 0 :
            p1 += 2 * pi

        if p2 < 0:
            p2 += 2 * pi

        angle = abs(p1 - p2)
        if angle > pi:
            angle = abs( angle - 2* pi )


        return  angle / pi * 180, p1 > p2

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.x*10000 + self.y)

    def __repr__(self):
        return f"({self.x},{self.y})"
