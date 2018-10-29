from PySide2 import QtGui, QtCore, QtWidgets

from ui.GamePages import AbstractPage

class StartPage(AbstractPage):
    """docstring for StartPage."""
    def __init__(self, gamePages):
        super().__init__()
        self.gamePages = gamePages
        self.arg = None
        self.w = 240
        self.h = 300
        self.setUpWidgets()

    def setUpWidgets(self):
        self.background = QtWidgets.QGraphicsRectItem(0, 0, self.gamePages.gameRoot.cfg.dev_size[0], self.gamePages.gameRoot.cfg.dev_size[1])
        self.background.setBrush(QtGui.QBrush(QtCore.Qt.black))
        self.addToGroup(self.background)

        self.mainWidget: QtWidgets.QGraphicsWidget = QtWidgets.QGraphicsWidget(self)
        self.mainWidget.resize(self.w, self.h)

        self.laoyout :QtWidgets.QGraphicsLinearLayout = QtWidgets.QGraphicsLinearLayout(QtCore.Qt.Vertical)
        buttonStyle = 'QPushButton{background-color:black;color:white;}QPushButton:pressed{background-color:white;color:black;}'

        self.start = QtWidgets.QPushButton('START')
        self.start.setStyleSheet(buttonStyle)
        self.start = self.gamePages.gameRoot.scene.addWidget(self.start)
        self.laoyout.addItem(self.start)
        self.start.setParent(self.mainWidget)

        self.stop = QtWidgets.QPushButton('STOP')
        self.stop.setStyleSheet(buttonStyle)
        self.stop:QtWidgets.QGraphicsProxyWidget = self.gamePages.gameRoot.scene.addWidget(self.stop)
        self.laoyout.addItem(self.stop)
        self.stop.setParent(self.mainWidget)

        self.settings = QtWidgets.QPushButton('SETTINGS')
        self.settings.setStyleSheet(buttonStyle)
        self.settings:QtWidgets.QGraphicsProxyWidget = self.gamePages.gameRoot.scene.addWidget(self.settings)
        self.laoyout.addItem(self.settings)
        self.settings.setParent(self.mainWidget)

        self.mainWidget.setLayout(self.laoyout)
        self.addToGroup(self.mainWidget)
        self.gamePages.gameRoot.scene.addItem(self)
        # self.setVisible(False)
        self.resized()

    def showPage(self):
        if self.state:
            self.state = False
            # self.setVisible(False)
            self.gamePages.page = None
            self.gamePages.gameRoot.scene.removeItem(self)
        else:
            self.state = True
            self.gamePages.page = self
            self.gamePages.gameRoot.scene.addItem(self)
            # self.setVisible(True)

    def widgetShape(cls):
        path = QtGui.QPainterPath()
        path.addRect(cls.boundingRect())
        return path

    def widgetMousePressEvent(cls, e):
        if cls.boundingRect().contains(e.pos()):
            cls.pressed.emit()

    def resized(self):
        x = (self.gamePages.gameRoot.cfg.dev_size[0] - self.w) / 2
        y = (self.gamePages.gameRoot.cfg.dev_size[1] - self.h) / 2
        self.mainWidget.moveBy(x, y)
        self.mainWidget.setPos(x, y)
        self.background.setRect(0, 0, self.gamePages.gameRoot.cfg.dev_size[0], self.gamePages.gameRoot.cfg.dev_size[1])
        pass

    def mousePressEvent(self, e):
        if self.mainWidget.geometry().contains(e.pos()):
            self.containsWidget(self.start, e)
            self.containsWidget(self.stop, e)
            self.containsWidget(self.settings, e)

    def containsWidget(self, widgetProxy, e):
        rect = widgetProxy.geometry()
        rect.translate(widgetProxy.parent().pos())
        if rect.contains(e.pos()):
            widgetProxy.widget().pressed.emit()
            widgetProxy.widget().setDown(True)

    def mouseReleaseEvent(self, e):
        self.mainWidget.mouseReleaseEvent(e)
        self.start.mouseReleaseEvent(e)
        self.stop.mouseReleaseEvent(e)
        self.settings.mousePressEvent(e)

    def startSlot(self):
        self.gamePages.page = self.gamePages.gameMenu
        self.gamePages.page.resized()
        self.gamePages.gameRoot.scene.removeItem(self)

    # def hide(self):
    #     self.gamePages.page = self.gamePages.gameMenu
    #     self.gamePages.page.resized()
    #     super(StartPage, self).hide()





