from PySide2 import QtWidgets, QtCore

from ui.gamecore import GameObject
from ui.GameAnimation import Direction


from battlefield.Facing import Facing

from ui.GameAnimation import SmoothAnimation

class BasicUnit(GameObject):
    """docstring for BasicUnit."""
    def __init__(self, *arg, gameconfig):
        super(BasicUnit, self).__init__(*arg)
        self.uid = 0
        self.gameconfig = gameconfig
        self.setUpDirections()
        self.activate = False
        self.hp = 100
        self.dir_angle = Facing.SOUTH

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
        self.dirAni = SmoothAnimation(self.direction, self.direction.setRotation)


    dir_dict = {(Facing.SOUTH, Facing.EAST) : (360., 270.),
                (Facing.SOUTH, Facing.WEST): (0., 90.),
                (Facing.EAST, Facing.SOUTH): (270., 360.),
                (Facing.WEST, Facing.SOUTH): (90., 0.),

                (Facing.NORTH, Facing.EAST): (180., 270.),
                (Facing.NORTH, Facing.WEST): (180., 90.),
                (Facing.EAST, Facing.NORTH): (270., 180.),
                (Facing.WEST, Facing.NORTH): (90., 180.),
                }
    def setDirection(self, turn):
        if turn != self.dir_angle:
            start, end = BasicUnit.dir_dict[(self.dir_angle, turn)]
            self.dirAni.play_anim(start, end)
            self.dir_angle = turn

    def __eq__(self, other):
        if self is other: return True
        if other is None: return False
        if self.__class__ != other.__class__: return False
        return self.worldPos == other.worldPos.x

    def __hash__(self):
        return hash(self.worldPos)*3

    def __repr__(self):
        return f"{self.worldPos} -> BasicUnit {self.uid} "
