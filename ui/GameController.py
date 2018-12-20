from battlefield import Cell
from PySide2 import QtCore, QtGui, QtWidgets
from battlefield.Facing import Facing

from ui.events import UiErrorMessageEvent
from exceptions import PydolonsException
from ui.TransformSupport import TransformSupport


class GameController(QtCore.QObject):
    keyPress = QtCore.Signal(QtCore.QEvent)
    mouseRelease = QtCore.Signal()
    mousePress = QtCore.Signal(QtCore.QEvent)
    mouseMove = QtCore.Signal(QtCore.QEvent)

    def __init__(self):
        super(GameController, self).__init__()
        """
        last_point = Cell() -- последняя точка, на которую указывает игрок
        """
        self.gameRoot = None
        self.tr = QtGui.QTransform()
        self.tr_support:TransformSupport = None

        self.cursor = QtWidgets.QGraphicsEllipseItem(-10, -10, 20, 20)

        self.last_point = Cell(0, 0)
        self.selected_point = Cell(0, 0)
        self.lost_m_pos = QtCore.QPoint()
        self.r_mouse = False


    def setGameRoot(self, gameRoot):
        self.tr_support = TransformSupport(gameRoot)
        gameRoot.view.resized.connect(self.tr_support.resized)
        self.gameRoot = gameRoot
        self.gameRoot.controller = self

    def setUp(self, world, units, middleLayer):
        self.world = world
        self.units = units
        self.middleLayer = middleLayer

    def moveCursor(self, newPos):
        self.cursor.setX(newPos.x())
        self.cursor.setY(newPos.y())

    def mouseMoveEvent(self, e):
        """ Метод перехватывает событие движение мыши
        """
        self.mouseMove.emit(e)
        if not self.gameRoot.gamePages.isGamePage:
            if not self.gameRoot.gamePages.gameMenu.isFocus():
                pos = self.gameRoot.view.mapToScene(e.pos().x(), e.pos().y())
                self.lost_m_pos.setX(pos.x())
                self.lost_m_pos.setY(pos.y())
                if self.tr_support.floor_rect.contains(pos.x(), pos.y()):
                    self.moveCursor(pos)
                    self.itemSelect(pos)
        self.tr_support.mouseMoveEvent(e)

    def mousePressEvent(self, e):
        self.mousePress.emit(e)
        self.tr_support.mousePressEvent(e)
        if e.button() == QtCore.Qt.RightButton:
            self.r_mouse = True
            try:
                if not self.gameRoot.gamePages.isGamePage:
                    if self.tr_support.floor_rect.contains(self.lost_m_pos.x(), self.lost_m_pos.y()):
                        self.gameRoot.game.ui_order(self.last_point.x, self.last_point.y)
                        self.selected_point.x, self.selected_point.y = self.last_point.x, self.last_point.y
                        self.middleLayer.showSelectedItem(self.selected_point.x, self.selected_point.y)
            except PydolonsException as exc:
                UiErrorMessageEvent(self.gameRoot.game, repr(exc))

    def mouseReleaseEvent(self, e):
        self.tr_support.mouseReleaseEvent(e)
        self.r_mouse = False
        self.mouseRelease.emit()

    def keyPressEvent(self, e):
        self.keyPress.emit(e)
        try:
            self.order_from_hotkey(e)
        except PydolonsException as exc:
            UiErrorMessageEvent(self.gameRoot.game, repr(exc))

    def wheelEvent(self, e):
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
        self.middleLayer.showToolTip(self.last_point,
                                     self.units.units_at,
                                     self.gameRoot.game.battlefield.units_at)
        self.middleLayer.selectItem(x, y)

    orientations = {
        QtCore.Qt.Key_W: Facing.EAST,
        QtCore.Qt.Key_A: Facing.NORTH,
        QtCore.Qt.Key_S: Facing.WEST,
        QtCore.Qt.Key_D: Facing.SOUTH,

        QtCore.Qt.Key_Up: Facing.EAST,
        QtCore.Qt.Key_Left: Facing.NORTH,
        QtCore.Qt.Key_Down: Facing.WEST,
        QtCore.Qt.Key_Right: Facing.SOUTH,
    }

    def order_from_hotkey(self, e):
        if e.key() == QtCore.Qt.Key_Q:
            self.gameRoot.game.order_turn_ccw()
        elif e.key() == QtCore.Qt.Key_E:
            self.gameRoot.game.order_turn_cw()
        elif e.key() in GameController.orientations:
            self.gameRoot.game.order_step(GameController.orientations[e.key()])
        if self.middleLayer.targeted:
            self.middleLayer.removeTargets()

