from PySide2 import QtGui, QtCore, QtWidgets

from ui.GamePages import AbstractPage

from cntent.dungeons.small_orc_cave import small_orc_cave
from cntent.dungeons.pirate_lair import pirate_lair
from cntent.dungeons.demo_dungeon import demo_dungeon
from cntent.dungeons.demo_dungeon_walls import walls_dungeon
from cntent.dungeons.small_graveyard import small_graveyard

from DreamGame import DreamGame

class LevelSelect(AbstractPage):
    """docstring for LevelSelect."""
    def __init__(self, gamePages):
        super().__init__(gamePages)
        self.w = 600
        self.h = self.w
        self.y = 24
        self.x = 24
        self.dungeon_widgets = []
        self.fake_btns = []
        self.setUpWidgets([small_orc_cave, pirate_lair, small_graveyard, demo_dungeon, walls_dungeon])
        self.defaultGame = True
        self.isService = True

    def setUpGui(self):
        self.cancel.pressed.connect(self.cancelSlot)


    def setUpWidgets(self, dung_list):
        self.background = QtWidgets.QGraphicsRectItem(0, 0, self.gamePages.gameRoot.cfg.dev_size[0], self.gamePages.gameRoot.cfg.dev_size[1])
        self.background.setBrush(QtGui.QBrush(QtCore.Qt.black))
        self.addToGroup(self.background)

        mainWidget: QtWidgets.QWidget = QtWidgets.QWidget()
        mainWidget.resize(self.w, self.h)
        mainWidget.setStyleSheet('background-color: rgba(0, 0, 0, 0);color:white')

        self.buttonStyle = 'QPushButton{background-color:grey;color:black;}QPushButton:pressed{background-color:white;color:black;}'

        mainLayout = QtWidgets.QHBoxLayout()

        layout = QtWidgets.QGridLayout()

        self.frame = QtWidgets.QWidget(mainWidget)
        self.frame.setFixedWidth(400)
        scrollArea = QtWidgets.QScrollArea(parent=mainWidget)
        scrollArea.setFixedWidth(420)



        for i, dungeon in enumerate(dung_list):
            dung_widg = self.getWidget(dungeon, mainWidget)
            layout.addWidget(dung_widg, i // 2, i % 2)
            self.dungeon_widgets.append(dung_widg)

            # dung_widg.selected.connect(self.select_dungeon)
            # dung_widg.deselected.connect(self.disable_start)

        self.cancel = QtWidgets.QPushButton("X", mainWidget)
        self.cancel.setStyleSheet(self.buttonStyle)

        # layout.addWidget(self.cancel)
        self.frame.setLayout(layout)
        scrollArea.setWidget(self.frame)
        mainLayout.addWidget(scrollArea)

        textScrolArea = QtWidgets.QScrollArea()
        textScrolArea.setFixedWidth(320)
        self.textWidget = QtWidgets.QLabel(parent=mainWidget)
        self.textWidget.setFixedWidth(300)
        self.textWidget.setWordWrap(True)
        textScrolArea.setWidget(self.textWidget)

        mainLayout.addWidget(textScrolArea)

        mainWidget.setLayout(mainLayout)
        self.mainWidget = self.gamePages.gameRoot.scene.addWidget(mainWidget)
        self.gamePages.gameRoot.scene.removeItem(self.mainWidget)
        self.resized()

    def getWidget(self, dungeon, parent):
        def startGame():
            name = dungeon.name
            print('start:', name)
            self.hidePage()
            self.gamePages.gameRoot.ui.setGame(name)
            self.gamePages.gameRoot.ui.startGame()

        frame:QtWidgets.QFrame = QtWidgets.QFrame(parent=parent)
        frame.setProperty('dungeon',  dungeon)
        frame.setObjectName("DungeonFrame")
        frame.setStyleSheet("#DungeonFrame {border: 2px solid black}")

        form_layout = QtWidgets.QFormLayout(parent = parent)

        icon = QtWidgets.QLabel(parent=parent)
        icon.setPixmap(self.gamePages.gameRoot.cfg.getPicFile(dungeon.icon))
        form_layout.addRow(icon)

        form_layout.addRow(QtWidgets.QLabel(dungeon.name, parent))

        locs = dungeon.unit_locations(DreamGame())
        n_units_label = QtWidgets.QLabel(f'{len([u for u in locs.keys() if not u.is_obstacle])}', parent)
        form_layout.addRow('Units in the dungeon:', n_units_label)

        max_xp_label = QtWidgets.QLabel(f'{max([u.xp for u in locs.keys() if not u.is_obstacle])}', parent)
        form_layout.addRow('Strongest enemy XP: ', max_xp_label)

        start = QtWidgets.QPushButton('start', parent)
        start.setStyleSheet(self.buttonStyle)
        start.pressed.connect(startGame)
        form_layout.addRow(start)
        self.fake_btns.append(start)

        frame.setLayout(form_layout)
        # return QtWidgets.QLabel(str(dungeon), parent=parent)
        # label = QtWidgets.QLabel('Label 1', parent=parent)
        # label.setStyleSheet('color:white')
        return frame

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

    def hidePage(self):
        self.state = False
        self.gamePages.page = None
        self.gamePages.visiblePage = False
        self.gamePages.gameRoot.scene.removeItem(self)
        self.gamePages.gameRoot.scene.removeItem(self.mainWidget)

    def resized(self):
        self.w = self.mainWidget.boundingRect().width()
        x = (self.gamePages.gameRoot.cfg.dev_size[0] - self.w) / 2
        y = (self.gamePages.gameRoot.cfg.dev_size[1] - self.h) / 2
        self.mainWidget.setPos(x, y)
        self.background.setRect(0, 0, self.gamePages.gameRoot.cfg.dev_size[0], self.gamePages.gameRoot.cfg.dev_size[1])
        pass

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            if self.state:
                self.hidePage()

    def mousePressEvent(self, e):
        for widget in self.dungeon_widgets:
            qr = QtCore.QRect(self.mainWidget.x() + self.frame.x() + widget.x(), self.mainWidget.y() + self.frame.y() + widget.y(), widget.size().width(), widget.size().height())
            if qr.contains(e.pos().x(), e.pos().y()):
                widget.setStyleSheet("#DungeonFrame {border: 2px solid blue}")
                self.selectDungeon(widget.property('dungeon'))
            else:
                widget.setStyleSheet("#DungeonFrame {border: 2px solid black}")


    def selectDungeon(self, dungeon):
        self.textWidget.setText(dungeon.tooltip_info)

    def cancelSlot(self):
        self.hidePage()
        self.gamePages.startPage.showPage()







