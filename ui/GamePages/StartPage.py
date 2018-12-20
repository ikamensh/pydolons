from PySide2 import QtGui, QtCore, QtWidgets

from ui.GamePages import AbstractPage

class StartPage(AbstractPage):
    """docstring for StartPage."""
    def __init__(self, gamePages):
        super().__init__(gamePages)
        self.state = True
        self.w = 240
        self.h = 300
        self.gamePages.gameRoot.scene.addItem(self)
        self.setUpWidgets()
        self.defaultGame = True
        self.isService = True
        self.gamePages.gameRoot.view.wheel_change.connect(self.updatePos)

    def setUpWidgets(self):
        self.background = QtWidgets.QGraphicsPixmapItem(self.gamePages.gameRoot.cfg.getPicFile('arena.jpg'))
        self.resizeBackground(self.background)
        self.addToGroup(self.background)

        mainWidget: QtWidgets.QWidget = QtWidgets.QWidget()
        mainWidget.resize(self.w, self.h)
        mainWidget.setStyleSheet('background-color: rgba(0, 0, 0, 0);')

        laoyout :QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout(mainWidget)
        buttonStyle = 'QPushButton{background-color:black;color:white;}QPushButton:pressed{background-color:white;color:black;}'

        self.newGame = QtWidgets.QPushButton('New Game', mainWidget)
        self.newGame.setStyleSheet(buttonStyle)
        self.newGame.clicked.connect(self.startNewGame)
        laoyout.addWidget(self.newGame)

        self.stop = QtWidgets.QPushButton('STOP', mainWidget)
        self.stop.setStyleSheet(buttonStyle)
        self.stop.clicked.connect(self.stopSlot)
        laoyout.addWidget(self.stop)

        self.levels = QtWidgets.QPushButton('Levels', mainWidget)
        self.levels.setStyleSheet(buttonStyle)
        self.levels.clicked.connect(self.levelsSlot)
        laoyout.addWidget(self.levels)

        self.readme = QtWidgets.QPushButton('README', mainWidget)
        self.readme.setStyleSheet(buttonStyle)
        self.readme.clicked.connect(self.readmeSlot)
        laoyout.addWidget(self.readme)

        settings = QtWidgets.QPushButton('SETTINGS', mainWidget)
        settings.setStyleSheet(buttonStyle)
        laoyout.addWidget(settings)

        mainWidget.setLayout(laoyout)
        self.mainWidget = self.gamePages.gameRoot.scene.addWidget(mainWidget)
        self.mainWidget.setFlags(QtWidgets.QGraphicsItem.ItemIgnoresTransformations)
        self.resized()

    def showPage(self):
        if self.state:
            if not self.gamePages.gameRoot.loop is None:
                self.state = False
                self.focusable.emit(False)
                self.gamePages.page = None
                self.gamePages.visiblePage = False
                self.gamePages.gameRoot.scene.removeItem(self)
                self.gamePages.gameRoot.scene.removeItem(self.mainWidget)
        else:
            self.state = True
            self.focusable.emit(True)
            self.gamePages.page = self
            self.gamePages.visiblePage = True
            self.gamePages.gameRoot.scene.addItem(self)
            self.gamePages.gameRoot.scene.addItem(self.mainWidget)


    def hidePage(self):
        self.state = False
        self.focusable.emit(False)
        self.gamePages.page = None
        self.gamePages.visiblePage = False
        self.gamePages.gameRoot.scene.removeItem(self)
        self.gamePages.gameRoot.scene.removeItem(self.mainWidget)

    def resized(self):
        super().resized()
        self.widget_pos.setX((self.gamePages.gameRoot.cfg.dev_size[0] - self.w) / 2)
        self.widget_pos.setY((self.gamePages.gameRoot.cfg.dev_size[1] - self.h) / 2)
        self.mainWidget.setPos(self.gamePages.gameRoot.view.mapToScene(self.widget_pos))
        self.resizeBackground(self.background)
        pass

    def startNewGame(self):
        self.gamePages.gameRoot.lengine.character = None
        self.hidePage()
        self.gamePages.levelSelect.showPage()

    def stopSlot(self):
        pass
        # print('stop')

    def levelsSlot(self):
        self.hidePage()
        self.gamePages.levelSelect.showPage()

    def readmeSlot(self):
        self.hidePage()
        self.gamePages.readme.showPage()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.showPage()
        pass

    def updatePos(self):
        super().updatePos()
        self.mainWidget.setPos(self.gamePages.gameRoot.view.mapToScene(self.widget_pos))



