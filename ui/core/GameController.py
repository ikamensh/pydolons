from __future__ import annotations

from battlefield import Cell
from PySide2 import QtCore, QtGui, QtWidgets
from battlefield.Facing import Facing

from ui.core.events import UiErrorMessageEvent
from exceptions import PydolonsError
from ui.core.TransformSupport import TransformSupport

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.core import GameRootNode
    from ui.pages.AbstractPage import AbstractPage
    from ui.world import GameWorld
    from ui.world.units import UnitMiddleLayer, Units


class GameController(QtCore.QObject):
    keyPress = QtCore.Signal(QtCore.QEvent)
    mouseRelease = QtCore.Signal()
    mousePress = QtCore.Signal(QtCore.QEvent)
    mouseMove = QtCore.Signal(QtCore.QEvent)

    def __init__(self, gameRoot):
        super(GameController, self).__init__()
        """
        last_point = Cell() -- последняя точка, на которую указывает игрок
        """
        self.gameRoot:GameRootNode = gameRoot
        self.tr = QtGui.QTransform()
        self.tr_support:TransformSupport = None

        self.cursor = QtWidgets.QGraphicsEllipseItem(-10, -10, 20, 20)

        self.last_point = Cell(0, 0)
        self.selected_point = Cell(0, 0)
        self.lost_m_pos = QtCore.QPointF()
        self.r_mouse = False
        self.observers = []
        self.orientations = {
            self.gameRoot.cfg.input_keys.east_move: Facing.EAST,
            self.gameRoot.cfg.input_keys.north_move: Facing.NORTH,
            self.gameRoot.cfg.input_keys.west_move: Facing.WEST,
            self.gameRoot.cfg.input_keys.south_move: Facing.SOUTH,
        }

    def setGameRoot(self, gameRoot):
        self.tr_support = TransformSupport(gameRoot)
        gameRoot.view.resized.connect(self.tr_support.resized)
        self.gameRoot = gameRoot
        self.gameRoot.controller = self

    def setUp(self, world, units, middleLayer):
        self.world: GameWorld = world
        self.units: Units = units
        self.middleLayer: UnitMiddleLayer = middleLayer

    def moveCursor(self, newPos):
        self.cursor.setX(newPos.x())
        self.cursor.setY(newPos.y())

    def mouseMoveEvent(self, e):
        """ Метод перехватывает событие движение мыши
        """
        self.mouseMove.emit(e)
        if not self.gameRoot.gamePages.isGamePage:
            if self.gameRoot.gamePages.gameMenu is not None:
                pos = self.gameRoot.view.mapToScene(e.pos().x(), e.pos().y())
                self.lost_m_pos.setX(pos.x())
                self.lost_m_pos.setY(pos.y())
                if self.tr_support.floor_rect.contains(pos.x(), pos.y()):
                    self.moveCursor(pos)
                    self.itemSelect(pos)
        if self.gameRoot.game is not None:
            self.tr_support.mouseMoveEvent(e)

    def mousePressEvent(self, e):
        # self.mousePress.emit(e)
        self.tr_support.mousePressEvent(e)
        if not self.tr_support.isMovable:
            if e.button() == QtCore.Qt.LeftButton:
                self.r_mouse = True
                try:
                    if not self.gameRoot.gamePages.isGamePage:
                        if self.tr_support.floor_rect.contains(self.lost_m_pos.x(), self.lost_m_pos.y()):
                            if self.gameRoot.game is not None:
                                self.gameRoot.game.ui_order(self.last_point.x, self.last_point.y)
                            self.selected_point.x, self.selected_point.y = self.last_point.x, self.last_point.y
                            self.middleLayer.showSelectedItem(self.selected_point.x, self.selected_point.y)
                except PydolonsError as exc:
                    UiErrorMessageEvent(self.gameRoot.game, repr(exc))

    def mouseReleaseEvent(self, e):
        self.tr_support.mouseReleaseEvent(e)
        self.r_mouse = False
        self.mouseRelease.emit()

    def keyPressEvent(self, e):
        self.keyPress.emit(e)
        try:
            self.send_key_press(e)
        except PydolonsError as exc:
            UiErrorMessageEvent(self.gameRoot.game, repr(exc))

    def wheelEvent(self, e):
        if self.gameRoot.game is not None:
            self.tr_support.wheelEvent()
        pass

    def moveScene(self, rect, x, y):
        rect.translate(x, y)
        self.gameRoot.scene.setSceneRect(rect)
        self.gameRoot.gameMenu.setDefaultPos()

    def translatScene(self, e):
        """Данный метод обеспечивает перемещение сцены внутри представления
         метод проверяет приблизился ли курсор к краю представления
        """
        rect = self.gameRoot.scene.sceneRect()
        if e.x() - 5.0 < 5.0:
            rect.translate(-10, 0)
            self.gameRoot.scene.setSceneRect(rect)
            self.gameRoot.gameMenu.setDefaultPos()

        if e.x() + 5.0 > self.gameRoot.view.viewport().width() - 5.0:
            rect.translate(10, 0)
            self.gameRoot.scene.setSceneRect(rect)
            self.gameRoot.gameMenu.setDefaultPos()

        if e.y() - 5.0 < 5.0:
            rect.translate(0, -10)
            self.gameRoot.scene.setSceneRect(rect)
            self.gameRoot.gameMenu.setDefaultPos()

        if e.y() + 5.0 > self.gameRoot.view.viewport().height() - 5.0:
            rect.translate(0, 10)
            self.gameRoot.scene.setSceneRect(rect)
            self.gameRoot.gameMenu.setDefaultPos()

    def itemSelect(self, pos):
        x = int((pos.x() - self.tr_support.tr.m31() - self.world.pos().x()) / self.gameRoot.cfg.unit_size[0])
        y = int((pos.y() - self.tr_support.tr.m32() - self.world.pos().y()) / self.gameRoot.cfg.unit_size[1])
        self.last_point.x, self.last_point.y = x, y
        self.middleLayer.selectItem(x, y)



    def key_press_event(self, e):
        if e.key() == self.gameRoot.cfg.input_keys.turn_ccw:
            self.gameRoot.game.order_turn_ccw()
        elif e.key() == self.gameRoot.cfg.input_keys.turn_cw:
            self.gameRoot.game.order_turn_cw()
        elif e.key() in self.orientations:
            self.gameRoot.game.order_step(self.orientations[e.key()])
        elif e.key() == self.gameRoot.cfg.input_keys.map_move:
            self.tr_support.setMovableMaps()

    # Template Observer

    def register(self, observer):
        self.observers.append(observer)

    def un_register(self, observer):
        self.observers.remove(observer)

    def send_key_press(self, event):
        for observer in self.observers:
            observer.key_press_event(event)
