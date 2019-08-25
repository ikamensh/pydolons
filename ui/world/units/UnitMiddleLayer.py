from __future__ import annotations

from PySide2 import QtWidgets, QtCore
from ui.world.units.Target import Target

from battlefield import Cell
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.core.gameconfig.GameConfiguration import GameConfiguration
    from ui.core.levels.BaseLevel import BaseLevel


class UnitMiddleLayer(QtWidgets.QGraphicsItemGroup):
    def __init__(self, gameconfig):
        super(UnitMiddleLayer, self).__init__()
        self.gameconfig: GameConfiguration = gameconfig
        # self.selected_item Синяя клетка
        self.selected_item=None
        self.w, self.h = self.gameconfig.unit_size[0], self.gameconfig.unit_size[1]
        self.setUpSelectItem()
        self.level: BaseLevel = None
        self.targeted = False

    def setLevel(self, level):
        self.level =  level
        self.level.middleLayer = self

    def setUp(self):
        self.level.gameRoot.pages.gameMenu.actives.setTargets.connect(self.getTargets)

    def setUpSelectItem(self):
        self.select_item = QtWidgets.QGraphicsRectItem()
        self.select_item.setRect(0, 0, self.w, self.h)
        self.select_item.setOpacity(0.5)
        self.select_item.setBrush(QtCore.Qt.red)
        self.addToGroup(self.select_item)
        # Создание синей клетки
        # self.selected_item = QtWidgets.QGraphicsRectItem()
        # self.selected_item.setRect(0, 0, self.w, self.h)
        # self.selected_item.setOpacity(0.3)
        # self.selected_item.setBrush(QtCore.Qt.blue)
        # self.selected_item.setVisible(False)
        # self.addToGroup(self.selected_item)

    def showSelectedItem(self, x, y):
        """
        :param x:
        :param y:
        :return:

        Когда передается х, у выбирается клетка и закрашивается синим
        """
        # self.selected_item.setX(x * self.w)
        # self.selected_item.setY(y * self.h)
        # self.selected_item.setVisible(True)
        if self.targeted:
            self.removeTargets()
        pass

    def selectItem(self, x, y):
        self.select_item.setX(x * self.w)
        self.select_item.setY(y * self.h)
        pass

    def getTargets(self, targets):
        self.targets = []
        for item in targets:
            if isinstance(item, Cell):
                self.addTarget(item)
            else:
                self.addTarget(item.cell)

    def addTarget(self, item):
        target = Target()
        target.setBrush(QtCore.Qt.green)
        target.w = self.w
        target.h = self.h
        target.setRect(0, 0, target.w, target.h)
        self.targets.append(target)
        self.addToGroup(target)
        target.setWorldPos(item.x, item.y)
        self.targeted = True

    def removeTargets(self):
        for item in self.targets:
            self.removeFromGroup(item)
        self.targets = []
        self.targeted = False

    def key_press_event(self, event=None):
        if self.targeted:
            self.removeTargets()
