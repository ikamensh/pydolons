from PySide2 import QtCore, QtWidgets, QtGui


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
        w = pixMap.width()
        h = pixMap.width()
        self.floor = QtWidgets.QGraphicsRectItem()
        self.floor.setBrush(QtGui.QBrush(pixMap))
        self.floor.setRect(0, 0, w * self.worldSize[0], h * self.worldSize[1])
        self.addToGroup(self.floor)
