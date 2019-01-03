from PySide2 import QtCore, QtWidgets

from ui.GamePages import AbstractPage
from ui.GamePages.suwidgets.CharacterWidget import CharacterWidget
from ui.GamePages.suwidgets.MasteriesWidget import MasteriesWidget
from ui.GamePages.suwidgets.perk_tree.QPerkTree import QPerkTree
from ui.GamePages.suwidgets.GameMsgBox import GameMsgBox

from game_objects.battlefield_objects import base_attributes


class ChaPage(AbstractPage):
    """docstring for CharacterPage."""
    def __init__(self, gamePages):
        super(ChaPage, self).__init__(gamePages)
        self.character = self.gamePages.gameRoot.lengine.character
        self.unit = None
        self.btns = {}
        self.w, self.h = 700, 550
        self.w_2 = int(self.w / 2)
        self.h_2 = int(self.h / 2)
        self.setUpWidgets()
        self.gamePages.gameRoot.view.wheel_change.connect(self.updatePos)

    def setUpWidgets(self):
        self.background = QtWidgets.QGraphicsPixmapItem(self.gamePages.gameRoot.cfg.getPicFile('arena.jpg'))
        self.resizeBackground(self.background)
        self.addToGroup(self.background)

        self.buttonStyle = 'QPushButton{background-color:grey;color:black;}QPushButton:pressed{background-color:white;color:black;}'

        mainWidget: QtWidgets.QWidget = QtWidgets.QWidget()
        mainWidget.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        mainWidget.setStyleSheet('background-color: rgba(0, 0, 0, 0);color:white')
        mainLayout: QtWidgets.QGridLayout = QtWidgets.QGridLayout()
        mainLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)

        self.charWidget = CharacterWidget(self, parent = mainWidget)
        self.masteriWidget = MasteriesWidget(self, parent = mainWidget)
        self.perkWidget = QPerkTree(self.gamePages.gameRoot.cfg, self.character.perk_trees[0], self.character, mainWidget)

        mainLayout.addWidget(self.charWidget, 0, 0, 1, 1)
        mainLayout.addWidget(self.perkWidget, 0, 3, 3, 1)
        mainLayout.addWidget(self.masteriWidget, 1, 0, 1, 3)
        mainLayout.addLayout(self.getPageBtnLayout(mainWidget), 2, 3, 1, 1, alignment = QtCore.Qt.AlignRight)

        mainWidget.setLayout(mainLayout)

        self.mainWidget = self.gamePages.gameRoot.scene.addWidget(mainWidget)
        self.mainWidget.setFlags(QtWidgets.QGraphicsItem.ItemIgnoresTransformations)
        self.gamePages.gameRoot.scene.removeItem(self.mainWidget)

        msgBox = GameMsgBox()
        msgBox.setGameConfig(self.gamePages.gameRoot.cfg)
        msgBox.setText('This character page')
        msgBox.setInformativeText('Change character elements and up hero')
        self.msgBox = self.gamePages.gameRoot.scene.addWidget(msgBox)
        self.gamePages.gameRoot.scene.removeItem(self.msgBox)
        self.updatePage()
        self.resized()

    def setUpGui(self):
        self.ok.clicked.connect(self.okSlot)
        self.save.clicked.connect(self.saveSlot)
        self.reset.clicked.connect(self.resetSlot)

    def getHeroLayout(self, parent):
        hero = self.gamePages.gameRoot.lengine.the_hero
        layout = QtWidgets.QGridLayout()
        layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        layout.setVerticalSpacing(0)
        layout.setHorizontalSpacing(0)
        layout.setColumnMinimumWidth(0, 70)
        icon = QtWidgets.QLabel(parent)
        pixmap = self.gamePages.gameRoot.cfg.getPicFile(hero.icon, 101002002)
        icon.setPixmap(pixmap)
        icon.setFixedSize(pixmap.size())
        layout.addWidget(icon, 0, 0, 1, 2, QtCore.Qt.AlignLeft)
        self.healthBar = self.getHeroItemBar(layout, parent, 1, 'Health:')
        self.manaBar = self.getHeroItemBar(layout, parent, 2, 'Mana:')
        self.staminaBar = self.getHeroItemBar(layout, parent, 3, 'Stamina:')
        return layout

    def getHeroItemBar(self, layout, parent, row, name):
        label = QtWidgets.QLabel(name, parent)
        label.setFixedWidth(50)
        layout.addWidget(label, row, 0, 1, 1, QtCore.Qt.AlignLeft)
        bar = QtWidgets.QProgressBar(parent)
        bar.setFixedWidth(100)
        bar.setTextVisible(False)
        layout.addWidget(bar, row,  1, 1, 1, QtCore.Qt.AlignLeft)
        barLabel = QtWidgets.QLabel('', parent)
        barLabel.setFixedWidth(50)
        layout.addWidget(barLabel, row, 2, 1, 1, QtCore.Qt.AlignLeft)
        bar.setProperty('label', barLabel)
        return bar

    def getAttributeLayout(self, attribute, parent):
        layout = QtWidgets.QVBoxLayout()
        subLayout = QtWidgets.QHBoxLayout()
        pixmap = self.gamePages.gameRoot.cfg.getPicFile(str(attribute.name).lower() + '.png', 101002001)
        pixmap = pixmap.scaled(32, 32)
        icon = QtWidgets.QLabel(parent)
        icon.setPixmap(pixmap)
        icon.setFixedSize(pixmap.size())
        subLayout.addWidget(icon)
        spnBox = QtWidgets.QSpinBox(parent=parent)
        spnBox.setMinimum(self.character.base_type.attributes[attribute])
        spnBox.valueChanged.connect(self.freePointsChanged)
        spnBox.setProperty('attribute', attribute)
        self.btns[attribute] = spnBox
        subLayout.addWidget(spnBox)
        label = QtWidgets.QLabel(str(attribute.name), parent)
        layout.addLayout(subLayout)
        layout.addWidget(label)
        return layout

    def getPointLayout(self, parent):
        layout = QtWidgets.QGridLayout()
        layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.freePointLabel = QtWidgets.QLabel(parent = parent)
        self.freePointLabel.setText('Free points: '+ str(self.character.free_attribute_points))
        layout.addWidget(self.freePointLabel, 0, 0, 1, 1, QtCore.Qt.AlignRight)
        i = 1
        row = 1
        for attribute in base_attributes:
            if i % 2 == 0:
                col = 0
            else:
                col = 1
                row += 1
            layout.addLayout(self.getAttributeLayout(attribute, parent), row, col)
            i += 1
        return layout

    def getPageBtnLayout(self, parent):
        btnLayout = QtWidgets.QHBoxLayout()
        self.ok = QtWidgets.QPushButton("Ok", parent)
        self.ok.setStyleSheet(self.buttonStyle)
        btnLayout.addWidget(self.ok)

        self.save = QtWidgets.QPushButton("Save", parent)
        self.save.setStyleSheet(self.buttonStyle)
        btnLayout.addWidget(self.save)

        self.reset = QtWidgets.QPushButton("Reset", parent)
        self.reset.setStyleSheet(self.buttonStyle)
        btnLayout.addWidget(self.reset)

        return btnLayout

    def updatePage(self):
        self.charWidget.updatePage()
        self.masteriWidget.updatePage()
        self.perkWidget.updatePage()
        pass

    def okSlot(self):
        self.comitToChacracter()
        self.updatePage()
        self.hidePage()

    def resetSlot(self):
        self.resetPage()
        self.updatePage()

    def saveSlot(self):
        self.comitToChacracter()
        self.updatePage()

    def resized(self):
        super().resized()
        self.w = self.mainWidget.widget().width()
        self.h = self.mainWidget.widget().height()
        self.widget_pos.setX((self.gamePages.gameRoot.cfg.dev_size[0] - self.w) / 2)
        self.widget_pos.setY((self.gamePages.gameRoot.cfg.dev_size[1] - self.h) / 2)
        self.mainWidget.setPos(self.gamePages.gameRoot.view.mapToScene(self.widget_pos))
        self.resizeBackground(self.background)
        pass

    def showPage(self):
        self.state = True
        self.gamePages.page = self
        self.gamePages.visiblePage = True
        self.gamePages.gameRoot.scene.addItem(self)
        self.gamePages.gameRoot.scene.addItem(self.mainWidget)
        self.gamePages.gameRoot.scene.addItem(self.msgBox)

    def hidePage(self):
        self.state = False
        self.gamePages.page = self.gamePages.gameMenu
        self.gamePages.visiblePage = False
        self.gamePages.gameRoot.scene.removeItem(self)
        self.gamePages.gameRoot.scene.removeItem(self.mainWidget)

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            if self.state:
                self.focusable.emit(False)
                self.hidePage()
                self.gamePages.startPage.hidePage()

    def destroy(self):
        self.mainWidget.widget().destroy()
        if not self.mainWidget.scene() is None:
            self.gamePages.gameRoot.scene.removeItem(self.mainWidget)
        del self.mainWidget
        pass

    def comitToChacracter(self):
        try:
            self.gamePages.gameRoot.lengine.character.commit()
        except Exception as er:
            print("D'ont commit character", er)

    def resetPage(self):
        self.gamePages.gameRoot.lengine.character.reset()
        pass

    def updatePos(self):
        super().updatePos()
        self.mainWidget.setPos(self.gamePages.gameRoot.view.mapToScene(self.widget_pos))
