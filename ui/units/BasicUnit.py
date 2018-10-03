from PySide2 import QtWidgets
from ui.gamecore import GameObject

from battlefield.Facing import Facing

class BasicUnit(GameObject):
    """docstring for BasicUnit."""
    def __init__(self, *arg, gameconfig):
        super(BasicUnit, self).__init__(*arg)
        self.uid = 0
        self.gameconfig = gameconfig
        self.directionPix = self.gameconfig.getPicFile('DIRECTION POINTER.png')
        self.setUpDirections()
        self.activate = False
        self.hp = 100

    def setUpDirections(self):
        """Метод отображает стрелку в определенном направлении
        """
        self.dirS = QtWidgets.QGraphicsPixmapItem(self)
        dirY = self.h - self.directionPix.height()
        dirX = (self.w / 2) - (self.directionPix.width() / 2)
        self.dirS.setPos(dirX, dirY)
        self.dirS.setPixmap(self.directionPix)
        self.dirS.setVisible(False)

        self.dirN = QtWidgets.QGraphicsPixmapItem(self)
        self.dirN.setPixmap(self.directionPix)
        dirY = self.directionPix.height()
        dirX = (self.w / 2) + (self.directionPix.width() / 2)
        self.dirN.setPos(dirX, dirY)
        self.dirN.setRotation(180.0)
        self.dirN.setVisible(False)

        self.dirW = QtWidgets.QGraphicsPixmapItem(self)
        self.dirW.setPixmap(self.directionPix)
        dirY = (self.h / 2) - (self.directionPix.height() / 2)
        dirX = self.directionPix.width()
        self.dirW.setPos(dirX, dirY)
        self.dirW.setRotation(90.0)
        self.dirW.setVisible(False)


        self.dirO = QtWidgets.QGraphicsPixmapItem(self)
        self.dirO.setPixmap(self.directionPix)
        dirY = (self.h / 2) + (self.directionPix.height() / 2)
        dirX = self.w - self.directionPix.width()
        self.dirO.setPos(dirX, dirY)
        self.dirO.setRotation(-90.0)
        self.dirO.setVisible(False)


    def setDirection(self, turn):
        if turn == Facing.SOUTH:
            self.dirS.setVisible(True)
            self.dirN.setVisible(False)
            self.dirW.setVisible(False)
            self.dirO.setVisible(False)
        elif turn == Facing.NORTH:
            self.dirS.setVisible(False)
            self.dirN.setVisible(True)
            self.dirW.setVisible(False)
            self.dirO.setVisible(False)
        if turn == Facing.EAST:
            self.dirS.setVisible(False)
            self.dirN.setVisible(False)
            self.dirW.setVisible(False)
            self.dirO.setVisible(True)
        elif turn == Facing.WEST:
            self.dirS.setVisible(False)
            self.dirN.setVisible(False)
            self.dirW.setVisible(True)
            self.dirO.setVisible(False)
        # else:
        #     raise Exception("turn has invalid value.")

    def __eq__(self, other):
        if self is other: return True
        if other is None: return False
        if self.__class__ != other.__class__: return False
        return self.worldPos == other.worldPos.x

    def __hash__(self):
        return hash(self.worldPos)*3

    def __repr__(self):
        return f"{self.worldPos} -> BasicUnit {self.uid} "
