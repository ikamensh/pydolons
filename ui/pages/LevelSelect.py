from PySide2 import QtCore, QtWidgets

from ui.pages import AbstractPage

from cntent.dungeons.small_orc_cave import small_orc_cave
from cntent.dungeons.pirate_lair import pirate_lair
from cntent.dungeons.demo_dungeon import demo_dungeon
from cntent.dungeons.demo_dungeon_walls import walls_dungeon
from cntent.dungeons.small_graveyard import small_graveyard
from cntent.dungeons.tel_razi_temple import tel_razi_temple
from cntent.dungeons.tel_razi_factory import tel_razi_factory
from cntent.dungeons.dark_wood import dark_wood
from cntent.dungeons.pirate_store import pirate_store


from DreamGame import DreamGame


class LevelSelect(AbstractPage):
    """docstring for LevelSelect."""
    def __init__(self, gamePages):
        super().__init__(gamePages)
        self.w = 600 * self.gamePages.gameRoot.cfg.scale_x
        self.h = self.w
        self.y = 24
        self.x = 24
        self.dungeon_widgets = []
        self.fake_btns = []
        self.setUpWidgets([small_orc_cave, pirate_lair, pirate_store, small_graveyard, demo_dungeon, walls_dungeon, tel_razi_temple, tel_razi_factory, dark_wood])
        self.defaultGame = True
        self.isService = True
        self.gamePages.gameRoot.view.wheel_change.connect(self.updatePos)

    def setUpWidgets(self, dung_list):
        self.background = QtWidgets.QGraphicsPixmapItem(self.gamePages.gameRoot.cfg.getPicFile('arena.jpg'))
        self.resizeBackground(self.background)
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
        self.mainWidget.setFlags(QtWidgets.QGraphicsItem.ItemIgnoresTransformations)
        self.gamePages.gameRoot.scene.removeItem(self.mainWidget)
        self.resized()

    def getWidget(self, dungeon, parent):
        def startGame():
            name = dungeon.name
            print('Select dungeon:', name)
            self.hidePage()
            self.gamePages.gameRoot.lengine.dungeon = dungeon
            self.gamePages.gameRoot.ui.startCharacterPage()

        frame:QtWidgets.QFrame = QtWidgets.QFrame(parent=parent)
        frame.setProperty('dungeon',  dungeon)
        frame.setObjectName("DungeonFrame")
        frame.setStyleSheet("#DungeonFrame {border: 2px solid black}")

        form_layout = QtWidgets.QFormLayout(parent = parent)

        icon = QtWidgets.QLabel(parent=parent)
        icon.setPixmap(self.gamePages.gameRoot.cfg.getPicFile(dungeon.icon))
        form_layout.addRow(icon)

        form_layout.addRow(QtWidgets.QLabel(dungeon.name, parent))

        objs = dungeon.construct_objs(DreamGame())
        n_units_label = QtWidgets.QLabel(f'{len([u for u in objs if not u.is_obstacle])}', parent)
        form_layout.addRow('Units in the dungeon:', n_units_label)

        max_xp_label = QtWidgets.QLabel(f'{max([u.xp for u in objs if not u.is_obstacle])}', parent)
        form_layout.addRow('Strongest enemy XP: ', max_xp_label)

        start = QtWidgets.QPushButton('start', parent)
        start.setStyleSheet(self.buttonStyle)
        start.clicked.connect(startGame)
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
        self.gamePages.page = None
        self.gamePages.visiblePage = False
        self.gamePages.gameRoot.scene.removeItem(self)
        self.gamePages.gameRoot.scene.removeItem(self.mainWidget)

    def resized(self):
        super().resized()
        self.w = self.mainWidget.boundingRect().width()
        self.widget_pos.setX((self.gamePages.gameRoot.cfg.dev_size[0] - self.w) / 2)
        self.widget_pos.setY((self.gamePages.gameRoot.cfg.dev_size[1] - self.h) / 2)
        self.mainWidget.setPos(self.widget_pos)
        self.resizeBackground(self.background)
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

    def updatePos(self):
        super().updatePos()
        self.mainWidget.setPos(self.gamePages.gameRoot.view.mapToScene(self.widget_pos))







