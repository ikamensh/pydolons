from PySide2 import QtWidgets

from battlefield import Cell


class Target(QtWidgets.QGraphicsRectItem):

    def __init__(self, *arg):
        super(Target, self).__init__(*arg)
        self.setOpacity(0.3)
        self.w, self.h = 1, 1
        self.worldPos = Cell(0, 0)

    def setWorldX(self, x):
        self.worldPos.x = x
        self.setX(x * self.w)

    def setWorldY(self, y):
        self.worldPos.y = y
        self.setY(y * self.h )

    def setWorldPos(self, x, y):
        self.setWorldX(x)
        self.setWorldY(y)
