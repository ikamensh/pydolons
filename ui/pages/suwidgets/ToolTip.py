from __future__ import annotations

from PySide2 import QtCore, QtWidgets

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.core.GameRootNode import GameRootNode


class ToolTip(QtCore.QObject, QtWidgets.QGraphicsRectItem):
    """docstring for ToolTip.

    Размер тултипа автоматически подстраивается
    в методе setText(self, text)
    self.minimuWidth -- минимальная ширина тултипа, устанвливает в методе setFont()
    self.minimuWidth Зависит от шрифта и self.minimumLeters -- минимальное количество символов

    """
    def __init__(self, gameRoot, parent=None):
        QtCore.QObject.__init__(self, parent)
        QtWidgets.QGraphicsRectItem.__init__(self, parent)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIgnoresTransformations, True)
        self.textItem = QtWidgets.QGraphicsTextItem()
        self.textItem.setParentItem(self)
        self.minimuWidth = 100
        self.minimumLeters = 16
        self._x = 0
        self._y = 0
        self.view_pos = QtCore.QPoint(0, 0)
        self.gameRoot: GameRootNode = gameRoot

    def setDefaultTextColor(self, color):
        self.textItem.setDefaultTextColor(color)

    def setFont(self, font):
        self.textItem.setFont(font)
        tempText = self.textItem.toPlainText()
        self.textItem.setPlainText("#" * self.minimumLeters)
        self.minimuWidth = self.textItem.boundingRect().width()
        self.textItem.setPlainText(tempText)

    def setPos(self, *args):
        if len(args) == 1:
            pos = args[0]
            self.view_pos = self.gameRoot.view.mapFromScene(pos)
            super(ToolTip, self).setPos(pos)
        elif len(args) == 2:
            self.view_pos = self.gameRoot.view.mapFromScene(args[0], args[1])
            super(ToolTip, self).setPos(args[0], args[1])

    def setTextPos(self, x, y):
        self.view_pos = self.gameRoot.view.mapFromScene(x, y)
        self.textItem.setPos(x, y)

    def setText(self, text):
        self.textItem.setPlainText(text)
        h = self.textItem.boundingRect().height()
        self.setRect(self.textItem.x(), self.textItem.y(), self.minimuWidth, h)

    def setDict(self, data):
        result = ''
        for k, v in data.items():
            result = result + k + ' = ' + v + '\n'
        self.setText(result[:-1])

    def wheel_change(self):
        self.setPos(self.gameRoot.view.mapToScene(self.view_pos))
