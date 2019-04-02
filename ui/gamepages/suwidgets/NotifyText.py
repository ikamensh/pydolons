from __future__ import annotations

from PySide2 import QtCore, QtWidgets

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.gamecore.GameRootNode import GameRootNode


class NotifyText(QtWidgets.QGraphicsTextItem):
    def __init__(self, parent = None):
        QtWidgets.QGraphicsTextItem.__init__(self, parent)
        self.gameRoot: GameRootNode = None
        self.setFlag(QtWidgets.QGraphicsItem.ItemIgnoresTransformations, True)
        self.setVisible(False)
        self.anim = QtCore.QPropertyAnimation(self, b'opacity')
        self.anim.setDuration(1000)
        self.anim.setStartValue(1.0)
        self.anim.setEndValue(0.0)
        self.anim.finished.connect(self.hide)
        self.widget_pos = (0, 0)

    def showText(self, text):
        self.setOpacity(1.0)
        self.setPlainText(str(text))
        x = self.gameRoot.cfg.dev_size[0] - self.boundingRect().width()
        y = self.gameRoot.cfg.dev_size[1] - self.boundingRect().height()
        x = x / 2
        y = y / 2
        self.widget_pos = x, y
        self.setPos(self.gameRoot.view.mapToScene(x, y))
        self.show()
        self.anim.start()

    def resized(self):
        self.setPos(self.gameRoot.view.mapToScene(self.widget_pos[0], self.widget_pos[1]))
        pass
