from PySide2 import QtGui, QtCore, QtWidgets

from ui.GamePages import AbstractPage
"""

function for GamePages

    def setUpDefaultPage(self):
        self.defaultPage = self.buildPage('defaultPage', DefaultPage)


"""


class DefaultPage(AbstractPage):
    """docstring for DefaultPage.
    self.mainWidget.widget() -- native Qt Widget
    self.mainWidget -- QGarphicsScene ProxyWidget

    """

    def __init__(self, gamePages):
        super().__init__(gamePages)
        self.w = 320
        self.h = 480
        self.setUpWidgets()
        pass

    def setUpWidgets(self):
        #  SetUp background
        self.background = QtWidgets.QGraphicsRectItem(
            0,
            0,
            self.gamePages.gameRoot.cfg.dev_size[0],
            self.gamePages.gameRoot.cfg.dev_size[1])
        self.background.setBrush(QtGui.QBrush(QtCore.Qt.black))
        self.addToGroup(self.background)

        self.buttonStyle = 'QPushButton{background-color:grey;color:black;}QPushButton:pressed{background-color:white;color:black;}'

        # Add main widget for Page
        mainWidget: QtWidgets.QWidget = QtWidgets.QWidget()
        mainWidget.resize(self.w, self.h)
        # SetUp opacity for main Widget
        mainWidget.setStyleSheet(
            'background-color: rgba(0, 0, 0, 0);color:white')
        # Add main Laout
        mainLayout: QtWidgets.QVBoxLayout = QtWidgets.QVBoxLayout()

        layout: QtWidgets.QHBoxLayout = QtWidgets.QHBoxLayout()

        self.ok = QtWidgets.QPushButton("ok", mainWidget)
        self.ok.setStyleSheet(self.buttonStyle)
        layout.addWidget(self.ok)

        self.cancel = QtWidgets.QPushButton("cancel", mainWidget)
        self.cancel.setStyleSheet(self.buttonStyle)
        layout.addWidget(self.cancel)

        self.label = QtWidgets.QLabel('Ok or Cancel?', parent=mainWidget)

        mainLayout.addWidget(self.label)
        mainLayout.addLayout(layout)

        mainWidget.setLayout(mainLayout)
        self.mainWidget = self.gamePages.gameRoot.scene.addWidget(mainWidget)

        self.resized()

    def resized(self):
        # automtical resize page
        x = (self.gamePages.gameRoot.cfg.dev_size[0] - self.w) / 2
        y = (self.gamePages.gameRoot.cfg.dev_size[1] - self.h) / 2
        self.mainWidget.setPos(x, y)
        self.background.setRect(0, 0, self.gamePages.gameRoot.cfg.dev_size[0],
                                self.gamePages.gameRoot.cfg.dev_size[1])
        pass

    def setUpGui(self):
        self.ok.pressed.connect(self.okSlot)
        self.cancel.pressed.connect(self.cancelSlot)

    def okSlot(self):
        print('ok press')

    def cancelSlot(self):
        print('cancel press')

    def keyPressEvent(self, e):
        # Hot key implementation
        #         if e.key() == QtCore.Qt.Key_Escape:
        #                 self.showPage()
        #
        #
        pass

    def showPage(self):
        if self.state:
            self.state = False
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

    def destroy(self):
        self.gamePages.gameRoot.scene.removeItem(self.mainWidget)
        del self.mainWidget
