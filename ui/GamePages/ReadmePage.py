from PySide2 import QtGui, QtCore, QtWidgets

from ui.GamePages import AbstractPage
from os import path


class ReadmePage(AbstractPage):
    """docstring for StartPage."""

    def __init__(self, gamePages):
        super().__init__(gamePages)
        self.w = 480
        self.h = 480
        self.isService = True
        self.setUpSize()
        self.setUpWidgets()
        self.gamePages.gameRoot.view.wheel_change.connect(self.updatePos)

    def setUpWidgets(self):
        self.background = QtWidgets.QGraphicsPixmapItem(
            self.gamePages.gameRoot.cfg.getPicFile('arena.jpg'))
        self.resizeBackground(self.background)
        self.addToGroup(self.background)
        self.scroll = QtWidgets.QGraphicsRectItem()
        brush = QtGui.QBrush(
            self.gamePages.gameRoot.cfg.getPicFile('scroll_background.png'))
        self.scroll.setBrush(brush)
        self.addToGroup(self.scroll)
        self.text = QtWidgets.QGraphicsTextItem()
        # self.getHtml()
        self.text.setHtml(self.getHtml())
        self.addToGroup(self.text)

    def getHtml(self):

        with open(path.join('resources', 'html', 'readme.html'), 'r') as f:
            return f.read()

    def setUpSize(self):
        self.w = int(
            (self.gamePages.gameRoot.cfg.dev_size[0] / 128) * 0.6) * 128
        self.h = int(
            (self.gamePages.gameRoot.cfg.dev_size[1] / 128) * 0.8) * 128

    def showPage(self):
        if self.state:
            self.state = False
            self.focusable.emit(False)
            self.gamePages.page = None
            self.gamePages.visiblePage = False
            self.gamePages.gameRoot.scene.removeItem(self)
            # self.gamePages.gameRoot.scene.removeItem(self.mainWidget)
        else:
            self.state = True
            self.focusable.emit(True)
            self.gamePages.page = self
            self.gamePages.visiblePage = True
            self.gamePages.gameRoot.scene.addItem(self)

    def hidePage(self):
        self.state = False
        self.gamePages.page = None
        self.gamePages.visiblePage = False
        self.gamePages.gameRoot.scene.removeItem(self)

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            if self.state:
                self.hidePage()

    def updatePos(self):
        super().updatePos()

    def resized(self):
        super().resized()
        self.setUpSize()
        self.widget_pos.setX(
            (self.gamePages.gameRoot.cfg.dev_size[0] - self.w) / 2)
        self.widget_pos.setY(
            (self.gamePages.gameRoot.cfg.dev_size[1] - self.h) / 2)
        pos = self.gamePages.gameRoot.view.mapToScene(self.widget_pos)
        self.scroll.setRect(pos.x(), pos.y(), self.w, self.h)
        self.text.setPos(pos)
        self.resizeBackground(self.background)
        pass
