from PySide2 import QtWidgets, QtCore

from ui.gamecore import GameObject
from ui.GameAnimation import Direction


from battlefield.Facing import Facing



class BasicUnit(GameObject):
    """docstring for BasicUnit."""
    def __init__(self, *arg, gameconfig):
        super(BasicUnit, self).__init__(*arg)
        self.uid = 0
        self.gameconfig = gameconfig
        self.setUpDirections()
        self.activate = False
        self.hp = 100
        self.dir_angle = 0

    def setUpDirections(self):
        """Метод отображает стрелку в определенном направлении
        """
        self.direction = Direction()
        self.direction.setParentItem(self)
        self.direction.setPixmap(self.gameconfig.getPicFile('DIRECTION POINTER.png'))
        self.direction.setTransformOriginPoint(self.direction.boundingRect().width()/2, - self.h/2 + self.direction.boundingRect().height())
        dirY = self.h - self.direction.boundingRect().height()
        dirX = (self.w / 2) - (self.direction.boundingRect().width() / 2)
        self.direction.setPos(dirX, dirY)
        self.dirAni = self.gameconfig.animations.getDirectionAnim(self.direction)


    def setDirection(self, turn):
        if turn == Facing.SOUTH:
            self.dirAni.setStartValue(self.direction.rotation())
            angel = 0.0
            if self.direction.rotation() == 270.0:
                angel = 360.0
            self.dirAni.setEndValue(angel)
            self.dirAni.start()
        elif turn == Facing.NORTH:
            self.dirAni.setStartValue(self.direction.rotation())
            self.dirAni.setEndValue(180.0)
            self.dirAni.start()
        if turn == Facing.EAST:
            angel = self.direction.rotation()
            if self.direction.rotation() == 0.0:
                angel = 360.0
            self.dirAni.setStartValue(angel)
            self.dirAni.setEndValue(270.0)
            self.dirAni.start()
        elif turn == Facing.WEST:
            angel = self.direction.rotation()
            if self.direction.rotation() == 360.0:
                angel = 0.0
            self.dirAni.setStartValue(angel)
            self.dirAni.setEndValue(90.0)
            self.dirAni.start()


    def __eq__(self, other):
        if self is other: return True
        if other is None: return False
        if self.__class__ != other.__class__: return False
        return self.worldPos == other.worldPos.x

    def __hash__(self):
        return hash(self.worldPos)*3

    def __repr__(self):
        return f"{self.worldPos} -> BasicUnit {self.uid} "
