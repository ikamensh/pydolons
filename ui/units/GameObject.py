from PySide2 import QtCore, QtWidgets

class GameObject(QtWidgets.QGraphicsPixmapItem):

    def __init__(self, w = 1, h = 1):
        super(GameObject, self).__init__()
        self.worldPos = QtCore.QPoint()
        self.w = w
        self.h = h


    def setWorldX(self, x):
        self.worldPos.setX(x)
        self.setX(x * self.w)


    def setWorldY(self, y):
        self.worldPos.setY(y)
        self.setY(y * self.h)


    def setWorldPos(self, x, y):
        self.setWorldX(x)
        self.setWorldY(y)


    def getWorldPos(self):
        return self.worldPos.x(), self.worldPos.y()
