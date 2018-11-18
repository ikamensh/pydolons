from PySide2 import QtCore, QtWidgets, QtGui

from ui.gamecore import GameObject

class ObstacleUnit(GameObject):
    """docstring for BasicUnit."""
    def __init__(self, *args):
        super(ObstacleUnit, self).__init__(*args)
        self.uid = 0
        self.activate = False
        self.hp = 100

    def __eq__(self, other):
        if self is other: return True
        if other is None: return False
        if self.__class__ != other.__class__: return False
        return self.worldPos == other.worldPos.x

    def __hash__(self):
        return hash(self.worldPos) * 5

    def __repr__(self):
        return f"{self.worldPos} -> ObstacleUnit {self.uid} "

class GameWorld(QtWidgets.QGraphicsItemGroup):
    def __init__(self, gameconfig):
        super(GameWorld, self).__init__()
        self.gameconfig = gameconfig
        self.size = QtCore.QRectF(0., 0., 1., 1.)
        self.worldSize = (1, 1)
        self.worldHalfSize = (1, 1)
        self.level = None
        self.obstacles = {}

    def setLevel(self, level):
        self.level = level
        self.level.world = self

    def setWorldSize(self, w, h):
        self.worldSize = (w, h)
        self.worldHalfSize = (int(w / 2), int(h / 2))
        self.size.setWidth(self.gameconfig.unit_size[0] * w)
        self.size.setHeight(self.gameconfig.unit_size[1] * h)
        x = (self.gameconfig.dev_size[0] - self.size.width()) / 2
        y = (self.gameconfig.dev_size[1] - self.size.height()) / 2
        # self.setPos(x, y)



    def setFloor(self, pixMap):
        self.floors = []
        for i in range(self.worldSize[0]):
            col = []
            for j in range(self.worldSize[1]):
                floor = GameObject(self.gameconfig.unit_size[0], self.gameconfig.unit_size[1])
                floor.setPixmap(pixMap)
                floor.setWorldPos(i, j)
                self.addToGroup(floor)
                col.append(floor)
                # self.floors =self.floors +col
            self.floors.append(col)
