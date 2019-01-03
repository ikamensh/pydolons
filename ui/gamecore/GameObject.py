from battlefield import Cell
from PySide2 import QtCore, QtWidgets


class GameObject(QtWidgets.QGraphicsPixmapItem):

    def __init__(self, w=1, h=1):
        """
        w, h -- задают ширину и высоту объекта
        self.pos() -- метод который возвращает текущее положение на сцене
        self.worldPos -- объект который задает положение в игровом мире не связанном с сценой
        """
        super(GameObject, self).__init__()
        self.worldPos = Cell(0, 0)
        self.w = w
        self.h = h
        self.is_hero = False
        self.is_obstacle = False

    def setWorldX(self, x):
        self.worldPos.x = x
        self.setX(x * self.w)

    def setWorldY(self, y):
        self.worldPos.y = y
        self.setY(y * self.h)

    def setWorldPos(self, x, y):
        self.setWorldX(x)
        self.setWorldY(y)

    def getWorldPos(self):
        return self.worldPos.x, self.worldPos.y
