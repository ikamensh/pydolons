class Cost:
    def __init__(self, stamina=0, mana=0, health=0, readiness = 1):
        self.stamina = stamina
        self.mana = mana
        self.health = health
        self.readiness = readiness

    def __mul__(self, other):

        return Cost(self.stamina * other,
                    self.mana * other,
                    self.health * other,
                    self.readiness * other)

    def __truediv__(self, other):
        return self.__mul__(1 / other)

    def __repr__(self):
        return f"{self.readiness} rdy, {self.stamina} sta, {self.mana} mp,  {self.health} hp"
