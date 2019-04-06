from ui.core import GameObject


class ObstacleUnit(GameObject):
    """docstring for ObstacleUnit."""
    def __init__(self, *args, name):
        super(ObstacleUnit, self).__init__(*args)
        self.uid = 0
        self.activate = False
        self.hp = 100
        self.state = True
        self.name = name
        self.is_obstacle = True

    def __eq__(self, other):
        if self is other: return True
        if other is None: return False
        if self.__class__ != other.__class__: return False
        return self.worldPos == other.worldPos.x

    def __hash__(self):
        return hash(self.worldPos) * 5

    def __repr__(self):
        return f"{self.worldPos} -> ObstacleUnit {self.uid} "