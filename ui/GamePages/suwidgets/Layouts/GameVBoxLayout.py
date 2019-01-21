from PySide2 import QtCore, QtWidgets
from ui.GamePages.suwidgets.Layouts.GameLayout import GameLayout


class GameVBoxLayout(GameLayout):
    def __init__(self):
        super(GameVBoxLayout, self).__init__()

    def addItem(self, item):
        self.items.append(item)

    def setGeometry(self):
        if len(self.items) == 0:
            return
        j = 0
        w = self.maxSizeWidget().width()
        h = 0
        for item in self.items:
            item.setPos(self._x, self._y + j * self._spacing + h)
            h += item.sizeHint().height()
            j += 1

    def sizeHint(self):
        s = QtCore.QSize(0, 0)
        n = len(self.items)
        if n > 0:
            s = QtCore.QSize(32, 32)
        for item in self.items:
            s = s.expandedTo(item.sizeHint())
        return n * s + n * QtCore.QSize(self._spacing, self._spacing)

    def maxSizeWidget(self):
        s = QtCore.QSize(0, 0)
        n = len(self.items)
        if n > 0:
            s = QtCore.QSize(32, 32)
        for item in self.items:
            s = s.expandedTo(item.sizeHint())
        return s