from PySide2 import QtGui, QtCore, QtWidgets

from ui.GamePages import AbstractPage
from game_objects.battlefield_objects import get_attrib_by_enum, enum_to_abbrev

class CharacterPage(AbstractPage):
    """docstring for CharacterPage."""
    def __init__(self, gamePages):
        super(CharacterPage, self).__init__(gamePages)
        self.character = None
        self.unit = None
        self.freePoints = 0
        self.points = {}
        self.w, self.h = 700, 550
        self.w_2 = int(self.w / 2)
        self.h_2 = int(self.h / 2)
        self.setUpWidgets()

    def setUpWidgets(self):
        hero = self.gamePages.gameRoot.game.the_hero
        self.background = QtWidgets.QGraphicsRectItem(0, 0, self.w, self.h)
        self.background.setBrush(QtGui.QBrush(QtCore.Qt.black))
        self.addToGroup(self.background)

        self.heroIcon = QtWidgets.QGraphicsPixmapItem(self.gamePages.gameRoot.cfg.getPicFile(hero.icon, 101002002))
        self.addToGroup(self.heroIcon)


        self.buttonStyle = 'QPushButton{background-color:grey;color:black;}QPushButton:pressed{background-color:white;color:black;}'

        mainWidget: QtWidgets.QWidget = QtWidgets.QWidget()
        mainWidget.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        # mainWidget.resize(self.w, self.h)
        mainWidget.setStyleSheet('background-color: rgba(0, 0, 0, 0);color:white')
        mainLayout: QtWidgets.QGridLayout = QtWidgets.QGridLayout()
        mainLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)

        mainLayout.addLayout(self.getHeroLayout(mainWidget), 0, 0, 1, 1, QtCore.Qt.AlignLeft)
        mainLayout.addLayout(self.getPointLayout(mainWidget), 0, 1, 1, 2, QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        mainLayout.addLayout(self.getPageBtnLayout(mainWidget), 1, 0, 1, 1, QtCore.Qt.AlignLeft)
        mainWidget.setLayout(mainLayout)

        self.mainWidget = self.gamePages.gameRoot.scene.addWidget(mainWidget)
        self.gamePages.gameRoot.scene.removeItem(self.mainWidget)
        self.resized()

    def setUpGui(self):
        self.cancel.pressed.connect(self.cancelSlot)
        self.ok.pressed.connect(self.okSlot)

    def getHeroLayout(self, parent):
        hero = self.gamePages.gameRoot.game.the_hero
        layout = QtWidgets.QGridLayout()
        layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        layout.setVerticalSpacing(0)
        layout.setHorizontalSpacing(0)
        layout.setColumnMinimumWidth(0, 70)
        self.healthBar = self.getHeroItemBar(layout, parent, 0, 'Health:')
        self.manaBar = self.getHeroItemBar(layout, parent, 1, 'Mana:')
        self.staminaBar = self.getHeroItemBar(layout, parent, 2, 'Stamina:')
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
        spnBox.valueChanged.connect(self.freePointsChanged)
        spnBox.setProperty('attribute', attribute)
        subLayout.addWidget(spnBox)
        label = QtWidgets.QLabel(str(attribute.name), parent)
        layout.addLayout(subLayout)
        layout.addWidget(label)
        return layout

    def getPointLayout(self, parent):
        charactrer = self.gamePages.gameRoot.lengine.character
        self.freePoints = charactrer.free_attribute_points
        layout = QtWidgets.QGridLayout()
        layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.freePointLabel = QtWidgets.QLabel(parent = parent)
        self.freePointLabel.setText('Free points: '+ str(self.freePoints))
        layout.addWidget(self.freePointLabel, 0, 0, 1, 1, QtCore.Qt.AlignRight)
        i = 1
        row = 1
        for attribute in enum_to_abbrev.keys():
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

        self.ok = QtWidgets.QPushButton("ok", parent)
        self.ok.setStyleSheet(self.buttonStyle)
        btnLayout.addWidget(self.ok)

        self.save = QtWidgets.QPushButton("save", parent)
        self.save.setStyleSheet(self.buttonStyle)
        btnLayout.addWidget(self.save)

        self.cancel = QtWidgets.QPushButton("cancel", parent)
        self.cancel.setStyleSheet(self.buttonStyle)
        btnLayout.addWidget(self.cancel)

        return btnLayout

    def updatePage(self):
        hero = self.gamePages.gameRoot.game.the_hero
        self.healthBar.setMaximum(hero.max_health)
        self.healthBar.setValue(hero.health)
        self.healthBar.property('label').setText(str(int(hero.health)))
        self.manaBar.setMaximum(hero.max_mana)
        self.manaBar.setValue(hero.mana)
        self.manaBar.property('label').setText(str(int(hero.mana)))
        self.staminaBar.setMaximum(hero.max_stamina)
        self.staminaBar.setValue(hero.stamina)
        self.staminaBar.property('label').setText(str(int(hero.stamina)))

    def cancelSlot(self):
        self.showPage()
        pass

    def okSlot(self):
        self.showPage()
        pass

    def resized(self):
        x = (self.gamePages.gameRoot.cfg.dev_size[0] - self.w) / 2
        y = (self.gamePages.gameRoot.cfg.dev_size[1] - self.h) / 2
        self.mainWidget.setPos(x, y)
        self.w = self.mainWidget.widget().width()
        self.h = self.mainWidget.widget().height()
        self.background.setRect(x, y, self.w, self.h)
        self.heroIcon.setPos(x + 50, y + 50)
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
            self.updatePage()
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

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_O:
            self.showPage()

    def mousePress(self, e):
        self.mousePos = e.pos()
        if self.state:
            focusState = self.mainWidget.widget().geometry().contains(e.pos().x(), e.pos().y())
            if focusState:
                self.focusable.emit(True)
            else:
                self.focusable.emit(False)
                self.hidePage()

    def destroy(self):
        self.mainWidget.widget().destroy()
        if not self.mainWidget.scene() is None:
            self.gamePages.gameRoot.scene.removeItem(self.mainWidget)
        del self.mainWidget
        pass

    def freePointsChanged(self, value):
        spnBox = self.mainWidget.widget().focusWidget()
        tmpValue = self.points.get(spnBox.property('attribute').name)
        if tmpValue is None:
            tmpValue = 0
        self.points[spnBox.property('attribute').name] = value
        res = 0
        for value in self.points.values():
            res += value
        self.freePoints = self.gamePages.gameRoot.lengine.character.free_attribute_points - res
        if self.freePoints < 0:
            spnBox.setValue(tmpValue)
            self.points[spnBox.property('attribute').name] = tmpValue
            if self.freePoints != 0:
                self.freePoints += 1
        self.freePointLabel.setText('Free points: ' + str(self.freePoints))

