from PySide2 import QtGui, QtCore, QtWidgets

from ui.GamePages import AbstractPage

class StartPage(AbstractPage):
    """docstring for StartPage."""
    def __init__(self, gamePages):
        super().__init__()
        self.gamePages = gamePages
        self.state = True
        self.w = 240
        self.h = 300
        self.gamePages.gameRoot.scene.addItem(self)
        self.setUpWidgets()

    def setUpWidgets(self):
        self.background = QtWidgets.QGraphicsRectItem(0, 0, self.gamePages.gameRoot.cfg.dev_size[0], self.gamePages.gameRoot.cfg.dev_size[1])
        self.background.setBrush(QtGui.QBrush(QtCore.Qt.black))
        self.addToGroup(self.background)

        mainWidget: QtWidgets.QWidget = QtWidgets.QWidget()
        mainWidget.resize(self.w, self.h)
        mainWidget.setStyleSheet('background-color: rgba(0, 0, 0, 0);')

        laoyout :QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout(mainWidget)
        buttonStyle = 'QPushButton{background-color:black;color:white;}QPushButton:pressed{background-color:white;color:black;}'

        self.start = QtWidgets.QPushButton('START', mainWidget)
        self.start.setStyleSheet(buttonStyle)
        laoyout.addWidget(self.start)

        self.stop = QtWidgets.QPushButton('STOP', mainWidget)
        self.stop.setStyleSheet(buttonStyle)
        self.stop.pressed.connect(self.stopSlot)
        laoyout.addWidget(self.stop)

        settings = QtWidgets.QPushButton('SETTINGS', mainWidget)
        settings.setStyleSheet(buttonStyle)
        laoyout.addWidget(settings)

        mainWidget.setLayout(laoyout)
        self.mainWidget = self.gamePages.gameRoot.scene.addWidget(mainWidget)
        self.resized()

    def showPage(self):
        if self.state:
            self.state = False
            self.gamePages.page = None
            self.gamePages.gameRoot.scene.removeItem(self)
            self.gamePages.gameRoot.scene.removeItem(self.mainWidget)
        else:
            self.state = True
            self.gamePages.page = self
            self.gamePages.gameRoot.scene.addItem(self)
            self.gamePages.gameRoot.scene.addItem(self.mainWidget)

    def resized(self):
        x = (self.gamePages.gameRoot.cfg.dev_size[0] - self.w) / 2
        y = (self.gamePages.gameRoot.cfg.dev_size[1] - self.h) / 2
        self.mainWidget.setPos(x, y)
        self.background.setRect(0, 0, self.gamePages.gameRoot.cfg.dev_size[0], self.gamePages.gameRoot.cfg.dev_size[1])
        pass

    def startSlot(self):
        self.gamePages.page.resized()
        self.showPage()
        self.gamePages.page = self.gamePages.gameMenu

    def stopSlot(self):
        print('stop')





