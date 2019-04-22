from PySide2 import QtCore, QtWidgets

from ui.pages import AbstractPage
from ui.pages.widgets.GameButton import GameButton
from ui.animation.AnimatedItem import AnimatedItem


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
        self.button_id = 0

    def setUpWidgets(self):
        self.buttons = []
        self.background = QtWidgets.QGraphicsPixmapItem(self.gamePages.gameRoot.cfg.getPicFile('arena.jpg'))
        self.resizeBackground(self.background)
        self.addToGroup(self.background)

        mainWidget = QtWidgets.QWidget()
        mainWidget.resize(self.w, self.h)
        mainWidget.setStyleSheet('background-color: rgba(0, 0, 0, 0);')

        laoyout = QtWidgets.QVBoxLayout(mainWidget)
        buttonStyle = 'QPushButton{background-color:black;color:white;}QPushButton:pressed{background-color:white;color:black;}'

        self.newGame = GameButton('New Game', mainWidget)
        self.newGame.setStyleSheet(buttonStyle)
        self.newGame.clicked.connect(self.startNewGame)
        self.newGame.hovered.connect(self.get_wig)
        self.buttons.append(self.newGame)
        laoyout.addWidget(self.newGame)

        self.stop = GameButton('STOP', mainWidget)
        self.stop.setStyleSheet(buttonStyle)
        self.stop.clicked.connect(self.stopSlot)
        self.stop.hovered.connect(self.get_wig)
        self.buttons.append(self.stop)
        laoyout.addWidget(self.stop)

        self.levels = GameButton('Levels', mainWidget)
        self.levels.setStyleSheet(buttonStyle)
        self.levels.clicked.connect(self.levelsSlot)
        self.levels.hovered.connect(self.get_wig)
        self.buttons.append(self.levels)
        laoyout.addWidget(self.levels)

        self.readme = GameButton('README', mainWidget)
        self.readme.setStyleSheet(buttonStyle)
        self.readme.clicked.connect(self.readmeSlot)
        self.readme.hovered.connect(self.get_wig)
        self.buttons.append(self.readme)
        laoyout.addWidget(self.readme)

        self.settings = GameButton('SETTINGS', mainWidget)
        self.settings.setStyleSheet(buttonStyle)
        self.settings.clicked.connect(self.settingsSlot)
        self.settings.hovered.connect(self.get_wig)
        self.buttons.append(self.settings)
        laoyout.addWidget(self.settings)

        self.exit = GameButton('EXIT', mainWidget)
        self.exit.setStyleSheet(buttonStyle)
        self.exit.clicked.connect(self.exitSlot)
        self.exit.hovered.connect(self.get_wig)
        self.buttons.append(self.exit)
        laoyout.addWidget(self.exit)

        mainWidget.setLayout(laoyout)
        self.mainWidget = self.gamePages.gameRoot.scene.addWidget(mainWidget)
        self.mainWidget.setFlags(QtWidgets.QGraphicsItem.ItemIgnoresTransformations)
        self.resized()
        self.setUpAnim()

    def setUpAnim(self):
        self.fire_one = AnimatedItem(cfg=self.gamePages.gameRoot.cfg)
        self.addToGroup(self.fire_one)
        self.fire_one.setPics('fire_plate')
        self.fire_one.animation(mode=True, framerate=25)

        self.fire_two = AnimatedItem(cfg=self.gamePages.gameRoot.cfg)
        self.addToGroup(self.fire_two)
        self.fire_two.setPics('fire_plate')
        self.fire_two.animation(mode=True, framerate=25)

        self.setButtonPos()
        self.setAnimPos(0)

    def setButtonPos(self):
        self.buttons_pos = []
        self.buttons_pos.append(self.getButtonPos(self.newGame))
        self.buttons_pos.append(self.getButtonPos(self.stop))
        self.buttons_pos.append(self.getButtonPos(self.levels))
        self.buttons_pos.append(self.getButtonPos(self.readme))
        self.buttons_pos.append(self.getButtonPos(self.settings))
        self.buttons_pos.append(self.getButtonPos(self.exit))

    def getButtonPos(self, button):
        x1 = self.mainWidget.pos().x() + button.pos().x() - 68
        x2 = self.mainWidget.pos().x() + button.pos().x() + button.width()
        y = self.mainWidget.pos().y() + button.pos().y() - 48
        return x1, x2, y

    def setAnimPos(self, button_id):
        self.fire_one.setPos(self.buttons_pos[button_id][0], self.buttons_pos[button_id][2])
        self.fire_two.setPos(self.buttons_pos[button_id][1], self.buttons_pos[button_id][2])

    def showPage(self):
        self.state = True
        self.focusable.emit(True)
        self.gamePages.page = self
        self.gamePages.visiblePage = True
        self.show()
        self.mainWidget.show()

    def hidePage(self):
        self.state = False
        self.focusable.emit(False)
        self.gamePages.page = None
        self.gamePages.visiblePage = False
        self.hide()
        self.mainWidget.hide()

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
        if self.gamePages.gameRoot.game is not None:
            print('Stop level:', self.gamePages.gameRoot.lengine.dungeon.name)
            self.gamePages.gameRoot.ui.stopGame()

    def levelsSlot(self):
        self.hidePage()
        self.gamePages.levelSelect.showPage()

    def readmeSlot(self):
        self.hidePage()
        self.gamePages.readme.showPage()

    def settingsSlot(self):
        self.hidePage()
        self.gamePages.settigsPage.showPage()

    def exitSlot(self):
        QtWidgets.QApplication.closeAllWindows()

    def mouseMoveEvent(self, e):
        print(e)

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.keyPressEsc()
        elif e.key() == QtCore.Qt.Key_Enter or e.key() == QtCore.Qt.Key_Return:
            self.buttons[self.button_id].clicked.emit()
        elif e.key() == QtCore.Qt.Key_Up:
            self.button_id -= 1
            if self.button_id < 0:
                self.button_id = 5
            self.setAnimPos(self.button_id)
        elif e.key() == QtCore.Qt.Key_Down:
            self.button_id += 1
            if self.button_id > 5:
                self.button_id = 0
            self.setAnimPos(self.button_id)
        pass

    def keyPressEsc(self):
        if self.isVisible():
            self.hidePage()
        else:
            self.showPage()
        if self.gamePages.pages.get('characterPage') is not None:
            if self.gamePages.pages['characterPage'].isVisible():
                self.gamePages.pages['characterPage'].hidePage()
            elif self.gamePages.gameMenu is None:
                self.gamePages.pages['characterPage'].showPage()
        if self.gamePages.gameMenu is not None:
            if self.gamePages.gameMenu.isVisible():
                self.showPage()
                self.gamePages.gameMenu.hide()
            else:
                self.gamePages.gameMenu.show()

    def updatePos(self):
        super().updatePos()
        self.mainWidget.setPos(self.gamePages.gameRoot.view.mapToScene(self.widget_pos))

    def get_wig(self, button):
        self.button_id = self.buttons.index(button)
        self.setAnimPos(self.button_id)
