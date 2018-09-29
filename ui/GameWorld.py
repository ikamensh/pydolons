from PySide2 import QtWidgets
from ui.gamecore import GameObject

class GameWorld(QtWidgets.QGraphicsItemGroup):
    def __init__(self, gameconfig):
        super(GameWorld, self).__init__()
        self.gameconfig = gameconfig
        self.worldSize = (1, 1)
        self.worldHalfSize = (1, 1)
        self.level = None

    def setLevel(self, level):
        self.level =  level
        self.level.world = self

    def setWorldSize(self, w, h):
        self.worldSize = (w, h)
        self.worldHalfSize = (int(w / 2), int(h / 2))

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
