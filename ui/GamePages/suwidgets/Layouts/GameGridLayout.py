from PySide2 import QtCore, QtWidgets
from ui.GamePages.suwidgets.Layouts.GameLayout import GameLayout


class GameGridLayout(GameLayout):
    def __init__(self):
        super(GameGridLayout, self).__init__()

    def addItem(self, item, row, col):
        self.items.append(item)
        self.items_pos[item] = (row, col)

    def setGeometry(self):
        if len(self.items) == 0:
            return
        s = self.maxSizeWidget()
        for item in self.items:
            j, i = self.items_pos[item]
            # w = item.sizeHint().width()
            # h = item.sizeHint().height()
            w = s.width()
            h = s.height()
            item.setPos(self._x + i * self._spacing + i * w, self._y + j * self._spacing + j * h)

    def sizeHint(self):
        s = QtCore.QSize(0, 0)
        n = len(self.items)
        j, i = self.maxInex()
        j, i = j+1, i+1
        if n > 0:
            s = QtCore.QSize(32, 32)
        for item in self.items:
            s = s.expandedTo(item.sizeHint())
        return QtCore.QSize(i*s.width() + i * self._spacing, j*s.height() + j * self._spacing)

    def maxInex(self):
        _i,_j = 0, 0
        for i,j in self.items_pos.values():
            if i > _i:
                _i = i
            if j > _j:
                _j = j
        return _i,_j

    def maxSizeWidget(self):
        s = QtCore.QSize(0, 0)
        n = len(self.items)
        if n > 0:
            s = QtCore.QSize(32, 32)
        for item in self.items:
            s = s.expandedTo(item.sizeHint())
        return s
