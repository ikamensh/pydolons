from PySide2 import QtCore

from ui.gamecore import GameObject
from ui.GameAnimation import Direction
from ui.GameAnimation import SmoothAnimation
from ui.GameAnimation import GameVariantAnimation
from ui.units.HealthBar import HealthBar
from ui.units.HealthText import HealthText

from battlefield.Facing import Facing

QObject = QtCore.QObject


class BasicUnit(QObject, GameObject):
    """docstring for BasicUnit."""
    hovered = QtCore.Signal(QtCore.QObject)
    hover_out = QtCore.Signal()

    def __init__(self, *arg, gameconfig, parent = None, unit_bf = None):
        QObject.__init__(self, parent)
        GameObject.__init__(self, *arg)
        self.uid = 0
        self.gameconfig = gameconfig
        self.setUpDirections()
        self.activate = False
        self.hp = 100
        self.dir_angle = Facing.SOUTH
        self.count = 0
        self.count_max = 1
        self.is_obstacle = False
        self.isHover = False
        if unit_bf is not None:
            if unit_bf.icon == 'hero.png':
                self.is_hero = True
        self.setUpSupports(unit_bf)
        self.anim_move = None

    def setUpDirections(self):
        """Метод отображает стрелку в определенном направлении
        """
        if self.gameconfig is not None:
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
        print(self.dir_angle, turn)
        if turn != self.dir_angle:
            start, end = self.dir_dict.get((self.dir_angle, turn), (0, 90))

            self.dirAni.play_anim(start, end)
            self.dir_angle = turn

    def mouseMove(self, event):
        if self.isVisible() and not self.parentItem() is None:
            if self.gameRoot.tr_support.rectHitGroupItem(self).contains(event.pos()):
                self.isHover = True
                self.hovered.emit(self)
            else:
                if self.isHover:
                    self.hover_out.emit()
                    self.isHover = False

    def setUpSupports(self, unit_bf):
        self.hpBar = HealthBar()
        self.hpBar.setParentItem(self)
        self.hpText = HealthText()
        self.hpText.setParentItem(self)
        if unit_bf is not None:
            self.w, self.h = self.gameconfig.unit_size[0], self.gameconfig.unit_size[1]
            self.hpBar.setColor(self)
            self.hpBar.setRect(0, self.h, self.w, 32)
            # hp.setPos(.pos())
            self.hpBar.setHP(self.getHPprec(unit_bf))
            self.hpText.setUnitPos(self.pos())
            self.hpText.setUpFont()
            self.hpText.setUpAnimation()

    def updateSupport(self, unit_bf, amount):
        self.hpBar.setHP(self.getHPprec(unit_bf))
        self.hpText.setText(amount)

    def getHPprec(self, unit):
        return (unit.health * 100)/unit.max_health

    def setScale(self, scale):
        super(BasicUnit, self).setScale(scale)
        if scale == 0.5:
            self.hpText.setScale(2.)
        else:
            self.hpText.setScale(1.)

    def setOffset(self, x, y):
        super(BasicUnit, self).setOffset(x, y)
        # self.hpBar.
        if x != 0.:
            offset = self.offset()
            self.hpBar.setOffset(offset.x(), offset.y())
            self.hpText.setOffset(offset.x(), offset.y())
        else:
            self.hpBar.setOffset(0, 0)
            self.hpText.setOffset(0, 0)

    def moveTo(self, x, y):
        self.anim_move.setStartValue(self.pos())
        self.worldPos.x = x
        self.worldPos.y = y
        self.anim_move.setEndValue(QtCore.QPointF(x * self.w, y * self.h))
        self.anim_move.start()

    def setUpAnimation(self):
        self.anim_move = GameVariantAnimation(self)
        self.anim_move.valueChanged.connect(self.setPos)
        self.anim_move.setDuration(GameVariantAnimation.DURATION_UNIT_MOVE)

    def __eq__(self, other):
        if self is other: return True
        if other is None: return False
        if self.__class__ != other.__class__: return False
        return self.__hash__() == other.__hash__()

    def __hash__(self):
        return hash(self.worldPos.x * 2 + self.worldPos.y * 3 + self.uid*4)*3

    def __repr__(self):
        return f"{self.worldPos} -> BasicUnit {self.uid}"
