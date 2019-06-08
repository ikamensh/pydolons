from __future__ import annotations

from PySide2 import QtCore

from ui.core import GameObject
from ui.animation import Direction
from ui.animation import SmoothAnimation
from ui.animation import GameVariantAnimation
from ui.animation import UnitAnimations
from ui.world.units.HealthBar import HealthBar
from ui.world.units.HealthText import HealthText

from battlefield.Facing import Facing

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_objects.battlefield_objects import Unit
    from ui.core.GameRootNode import GameRootNode
    from ui.core.gameconfig.GameConfiguration import GameConfiguration


class BasicUnit(QtCore.QObject, GameObject):
    """docstring for BasicUnit."""
    hovered = QtCore.Signal(QtCore.QObject)
    hover_out = QtCore.Signal()
    facings = {(Facing.SOUTH, Facing.EAST) : 270,
                (Facing.SOUTH, Facing.WEST): 90,
                (Facing.EAST, Facing.SOUTH): 0,
                (Facing.WEST, Facing.SOUTH): 0,

                (Facing.NORTH, Facing.EAST): 270,
                (Facing.NORTH, Facing.WEST): 90,
                (Facing.EAST, Facing.NORTH): 180,
                (Facing.WEST, Facing.NORTH): 180,

               (Facing.NORTH, Facing.SOUTH): 0,
               (Facing.SOUTH, Facing.NORTH): 180,
               (Facing.EAST, Facing.WEST): 90,
               (Facing.WEST, Facing.EAST): 270,
               }

    dir_dict = {(Facing.SOUTH, Facing.EAST): (360., 270.),
                (Facing.SOUTH, Facing.WEST): (0., 90.),
                (Facing.EAST, Facing.SOUTH): (270., 360.),
                (Facing.WEST, Facing.SOUTH): (90., 0.),

                (Facing.NORTH, Facing.EAST): (180., 270.),
                (Facing.NORTH, Facing.WEST): (180., 90.),
                (Facing.EAST, Facing.NORTH): (270., 180.),
                (Facing.WEST, Facing.NORTH): (90., 180.),
                }


    def __init__(self, *arg, gameRoot, parent = None, unit_bf = None):
        QtCore.QObject.__init__(self, parent)
        GameObject.__init__(self, *arg)
        self.setAcceptHoverEvents(True)
        self.uid = 0
        self.cfg: GameConfiguration = gameRoot.cfg
        self.gameRoot: GameRootNode = gameRoot
        self.direction: Direction = None
        self.setUpDirections()
        self.activate = False
        self.hp = 100
        self._facing: Facing = Facing.EAST
        self.count = 0
        self.count_max = 1
        self.is_obstacle = False
        self.is_alive = True
        self.isHover = False
        if unit_bf is not None:
            if unit_bf.icon == 'hero.png':
                self.is_hero = True
            self.setUpUnitAttr(unit_bf)
        self.setUpSupports(unit_bf)
        self.anim_move: GameVariantAnimation = None
        self.last_pos = QtCore.QPointF()
        self.unit_bf: Unit = unit_bf

    def setUpAnimation(self):
        # self.anim_move = GameVariantAnimation(self)
        # self.anim_move.valueChanged.connect(self.setPos)
        # self.anim_move.setDuration(GameVariantAnimation.DURATION_UNIT_MOVE)
        # self.anim_move.finished.connect(self.finish_anim)
        self.anim_move = UnitAnimations.create_move_animation(self)
        self.anim_move.animationAt(0).valueChanged.connect(self.setPos)
        self.anim_move.animationAt(1).valueChanged.connect(self.setOpacity)

    def setUpDirections(self):
        """Метод отображает стрелку в определенном направлении
        """
        if self.cfg is not None:
            self.direction = Direction()
            self.direction.setParentItem(self)
            self.direction.setPixmap(self.cfg.getPicFile('DIRECTION POINTER.png'))
            self.direction.setTransformOriginPoint(self.direction.boundingRect().width()/2, - self.h/2 + self.direction.boundingRect().height())
            dirY = self.h - self.direction.boundingRect().height()
            dirX = (self.w / 2) - (self.direction.boundingRect().width() / 2)
            self.direction.setPos(dirX, dirY)
            self.dirAni = SmoothAnimation(self.direction, self.direction.setRotation)

    def setUpUnitAttr(self, unit_bf:Unit):
        self.facing = unit_bf.facing
        self.uid = unit_bf.uid
        self.setPixmap(self.gameRoot.cfg.getPicFile(unit_bf.icon))

    @property
    def facing(self) -> Facing:
        return self._facing

    @facing.setter
    def facing(self, facing):
        angle = self.facings.get((self._facing, facing))
        if angle is not None:
            self.direction.setRotation(angle)
            self._facing = facing

    def setDirection(self, turn):
        start, end = 0, 90
        angels = self.dir_dict.get((self.facing, turn))
        if angels is None:
            print('broken turn:', self.facing, turn)
        else:
            start, end = angels
        self.dirAni.play_anim(start, end)
        self.facing = turn

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
            self.w, self.h = self.cfg.unit_size[0], self.cfg.unit_size[1]
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

    def sceneEvent(self, event):
        if event.type() is QtCore.QEvent.Type.GraphicsSceneHoverEnter:
            self.isHover = True
            pos = self.gameRoot.tr_support.groupToScene(self)
            self.gameRoot.gamePages.toolTip.setPos(pos[0], pos[1])
            self.gameRoot.gamePages.toolTip.setDict(self.tooltip_info())
            self.gameRoot.gamePages.toolTip.show()
        if event.type() is QtCore.QEvent.Type.GraphicsSceneHoverLeave:
            self.isHover = False
            self.gameRoot.gamePages.toolTip.hide()
        return True

    def tooltip_info(self):
        if self.unit_bf is None:
            return self.toolTip_dic
        else:
            return self.unit_bf.tooltip_info

    def moveTo(self, x, y):
        if self.isVisible():
            self.anim_move.animationAt(0).setStartValue(self.pos())
            self.anim_move.animationAt(0).setEndValue(QtCore.QPointF(x * self.w, y * self.h))
            self.anim_move.start()
        else:
            self.setWorldPos(x, y)

    def __eq__(self, other):
        if self is other:
            return True
        if other is None:
            return False
        if self.__class__ != other.__class__:
            return False
        return self.__hash__() == other.__hash__()

    def __hash__(self):
        return hash(self.worldPos.x * 2 + self.worldPos.y * 3 + self.uid*4)*3

    def __repr__(self):
        return f"{self.worldPos} -> BasicUnit {self.uid}"


