from PySide2 import QtGui, QtCore, QtWidgets

from ui.GamePages import AbstractPage
from ui.experimental.perk_tree.QPerkTree import QPerkTree

class PerksPage(AbstractPage):
    """docstring for DefaultPage.
    """
    def __init__(self, gamePages):
        super().__init__(gamePages)
        self.w = 320
        self.h = 600
        self.mousePos = QtCore.QPoint(0, 0)
        self.setUpWidgets()
        pass

    def setUpWidgets(self):
        self.background = QtWidgets.QGraphicsRectItem(0, 0, self.w, self.h)
        self.background.setBrush(QtGui.QBrush(QtCore.Qt.black))
        self.addToGroup(self.background)

        character = self.gamePages.gameRoot.lengine.character
        mainWidget = QtWidgets.QScrollArea()
        tree = QPerkTree(character.perk_trees[0], character, parent=mainWidget)
        mainWidget.setWidget(tree)
        self.w = tree.width() + 20
        mainWidget.setFixedSize(self.w, self.h)
        mainWidget.setStyleSheet('background-color: rgba(0, 0, 0, 0);color:white')
        self.mainWidget = self.gamePages.gameRoot.scene.addWidget(mainWidget)
        self.gamePages.gameRoot.scene.removeItem(self.mainWidget)
        self.resized()

    def resized(self):
        x = (self.gamePages.gameRoot.cfg.dev_size[0] - self.w) / 2
        y = (self.gamePages.gameRoot.cfg.dev_size[1] - self.h) / 2
        self.mainWidget.setPos(x, y)
        self.background.setRect(x, y, self.w, self.h)
        pass

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_P:
                self.showPage()
        pass

    def showPage(self):
        if self.state:
            self.state = False
            self.focusable.emit(False)
            self.gamePages.page = None
            self.gamePages.visiblePage = False
            self.gamePages.gameRoot.scene.removeItem(self)
            self.gamePages.gameRoot.scene.removeItem(self.mainWidget)
        else:
            self.state = True
            self.gamePages.page = self
            self.gamePages.visiblePage = True
            self.gamePages.gameRoot.scene.addItem(self)
            self.gamePages.gameRoot.scene.addItem(self.mainWidget)


    def hidePage(self):
        self.state = False
        self.gamePages.page = None
        self.gamePages.visiblePage = False
        self.gamePages.gameRoot.scene.removeItem(self)
        self.gamePages.gameRoot.scene.removeItem(self.mainWidget)

    def destroy(self):
        # self.gamePages.gameRoot.scene.removeItem(self.mainWidget)
        del self.mainWidget

    def mousePress(self, e):
        self.mousePos = e.pos()
        if self.state:
            focusState = self.mainWidget.widget().geometry().contains(e.pos().x(), e.pos().y())
            if focusState:
                self.focusable.emit(True)
            else:
                self.focusable.emit(False)
                self.hidePage()



