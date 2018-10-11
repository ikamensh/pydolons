from PySide2 import QtWidgets, QtCore

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
        self.dir_angle = 0

    def setUpDirections(self):
        """Метод отображает стрелку в определенном направлении
        """
        self.direction = QtWidgets.QGraphicsPixmapItem(self)
        self.direction.setParentItem(self)
        self.direction.setPixmap(self.directionPix)
        self.direction.setTransformOriginPoint(self.directionPix.width()/2, - self.h/2 + self.directionPix.height())
        dirY = self.h - self.directionPix.height()
        dirX = (self.w / 2) - (self.directionPix.width() / 2)
        self.direction.setX(dirX)
        self.direction.setY(dirY)
        self.direction.setVisible(True)
        # self.scene().addItem(self.direction)
        self.timer = QtCore.QTimeLine(2000)
        self.timer.setFrameRange(0, 100)
        self.animation = QtWidgets.QGraphicsItemAnimation()
        self.animation.setItem(self.direction)
        self.animation.setTimeLine(self.timer)

    def setDirection(self, turn):
        if turn == Facing.SOUTH:
            self.timer.start()
            # self.direction.setRotation(0)
            self.animation.setRotationAt(0.1, 0);
            # self.animation.setRotationAt(1, 0);
            self.dir_angle = 0
        elif turn == Facing.NORTH:
            # self.direction.setRotation(180)
            self.timer.start()
            # self.direction.setRotation(0)
            self.animation.setRotationAt(0.1, 180);
            self.dir_angle = 180
        if turn == Facing.EAST:
            self.timer.start()
            # self.direction.setRotation(0)
            self.animation.setRotationAt(0.1, -90);
            # self.direction.setRotation(-90)
            self.dir_angle = -90
        elif turn == Facing.WEST:
            self.timer.start()
            # self.direction.setRotation(0)
            self.animation.setRotationAt(0.1, 90);
            # self.direction.setRotation(90)
            self.dir_angle = 90


    def __eq__(self, other):
        if self is other: return True
        if other is None: return False
        if self.__class__ != other.__class__: return False
        return self.worldPos == other.worldPos.x

    def __hash__(self):
        return hash(self.worldPos)*3

    def __repr__(self):
        return f"{self.worldPos} -> BasicUnit {self.uid} "
