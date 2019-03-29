from PySide2 import QtWidgets

from ui.GamePages import AbstractPage


class BackGorundPage(AbstractPage):
    """docstring for StartPage."""

    def __init__(self, gamePages):
        super().__init__(gamePages)
        self.state = True
        self.setZValue(-10)
        self.setUpWidgets()
        self.gamePages.gameRoot.view.wheel_change.connect(self.updatePos)

    def setUpWidgets(self):
        self.background = QtWidgets.QGraphicsPixmapItem(
            self.gamePages.gameRoot.cfg.getPicFile('dungeon.jpg'))
        self.resizeBackground(self.background)
        self.addToGroup(self.background)

    def resized(self):
        super().resized()
        self.resizeBackground(self.background)
        pass
