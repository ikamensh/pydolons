from PySide2 import QtGui, QtCore, QtWidgets

from ui.GamePages import AbstractPage

class CharacterPage(AbstractPage):
    """docstring for CharacterPage."""
    def __init__(self, gamePages):
        super(CharacterPage, self).__init__(gamePages)
        self.character = None
        self.unit = None
        self.w, self.h = 700, 550
        self.w_2 = int(self.w / 2)
        self.h_2 = int(self.h / 2)
        self.setUpAttributes()
        self.setUpWidgets()


    def setUpAttributes(self):
        self.attributes = {}
        self.attributes['str_base'] = 'STREINGTH'
        self.attributes['end_base'] = 'ENDURANCE'
        self.attributes['prc_base'] = 'PERCEPTION'
        self.attributes['agi_base'] = 'AGILITY'
        self.attributes['int_base'] = 'INTELLIGENCE'
        self.attributes['cha_base'] = 'CHARISMA'
        self.attributes['max_health_base'] = 'HEALTH'
        self.attributes['max_mana_base'] = 'MANA'
        self.attributes['max_stamina_base'] = 'STAMINA'
        self.attributes['armor_base'] = 'ARMOR'
        self.attributes['resists_base'] = 'RESISTANCES'
        self.attributes['armor_base'] = 'ARMOR'
        self.attributes['melee_precision_base'] = 'PRECISION'
        self.attributes['melee_evasion_base'] = 'EVASION'

    def setUpWidgets(self):
        hero = self.gamePages.gameRoot.game.the_hero
        self.background = QtWidgets.QGraphicsRectItem(0, 0, self.w, self.h)
        self.background.setBrush(QtGui.QBrush(QtCore.Qt.black))
        self.addToGroup(self.background)

        self.heroIcon = QtWidgets.QGraphicsPixmapItem(self.gamePages.gameRoot.cfg.getPicFile(hero.icon))
        self.addToGroup(self.heroIcon)


        self.buttonStyle = 'QPushButton{background-color:grey;color:black;}QPushButton:pressed{background-color:white;color:black;}'

        mainWidget: QtWidgets.QWidget = QtWidgets.QWidget()
        mainWidget.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        mainWidget.resize(self.w, self.h)
        mainWidget.setStyleSheet('background-color: rgba(0, 0, 0, 0);color:white')
        mainLayout: QtWidgets.QGridLayout = QtWidgets.QGridLayout()
        mainLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)

        mainLayout.addLayout(self.getHeroLayout(mainWidget), 0, 0, 1, 1, QtCore.Qt.AlignLeft)
        mainLayout.addLayout(self.getPointLayout(mainWidget), 0, 1, 1, 2, QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        mainLayout.addLayout(self.getPageBtnLayout(mainWidget), 1, 0, 1, 1, QtCore.Qt.AlignLeft)
        mainLayout.addLayout(self.getMasteryLayout(mainWidget), 1, 1, 1, 3)
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
        # layout.setColumnStretch(0, -1)
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

    def getMasteryLayout(self, parent):
        layout = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel(parent)
        label.setText('Mastery')
        layout.addWidget(label)
        body = QtWidgets.QHBoxLayout()
        col_1 = QtWidgets.QVBoxLayout()
        col_1.addWidget(QtWidgets.QLabel('Battle', parent))
        body.addLayout(col_1)
        col_2 = QtWidgets.QVBoxLayout()
        col_2.addWidget(QtWidgets.QLabel('Magic', parent))
        body.addLayout(col_2)
        col_3 = QtWidgets.QVBoxLayout()
        col_3.addWidget(QtWidgets.QLabel('Mics', parent))
        body.addLayout(col_3)
        layout.addLayout(body)
        return layout


    def setAttributeLayout(self, layout, row,name, parent):
        labelInfo = QtWidgets.QLabel(name, parent)
        spnBox = QtWidgets.QSpinBox(parent = parent)
        # spnBox.setMaximumWidth(50)
        # spnBox.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        layout.addWidget(labelInfo, row, 0, 1, 1, QtCore.Qt.AlignLeft)
        layout.addWidget(spnBox, row, 1, 1, 1, QtCore.Qt.AlignLeft)



    def getPointLayout(self, parent):
        layout = QtWidgets.QGridLayout()
        layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.freePoint = QtWidgets.QLabel(parent = parent)
        self.freePoint.setText('Free points:')
        layout.addWidget(self.freePoint, 0, 0, 1, 1, QtCore.Qt.AlignRight)
        row = 1
        for key, name in self.attributes.items():
            self.setAttributeLayout(layout, row, name, parent)
            row += 1

        # print(layout.stretch(2))
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
