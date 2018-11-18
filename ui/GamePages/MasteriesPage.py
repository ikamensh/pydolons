from PySide2 import QtGui, QtCore, QtWidgets

from ui.GamePages import AbstractPage

from character.masteries.MasteriesEnumSimple import MasteriesEnum, MasteriesGroups

class MasteriesPage(AbstractPage):
    """docstring for DefaultPage.
    """
    def __init__(self, gamePages):
        super().__init__(gamePages)
        self.w = 480
        self.h = 320
        self.mousePos = QtCore.QPoint(0, 0)
        self.character = None
        self.buttonStyle = 'QPushButton{background-color:grey;color:black;}QPushButton:pressed{background-color:white;color:black;}'
        self.masteriesDict = {}
        self.label_size = self.getLabelSize()
        self.setUpWidgets()
        self.workMasteries = None
        pass

    def setUpWidgets(self):
        self.background = QtWidgets.QGraphicsRectItem(0, 0, self.w, self.h)
        self.background.setBrush(QtGui.QBrush(QtCore.Qt.black))
        self.addToGroup(self.background)

        character = self.gamePages.gameRoot.lengine.character
        self.character = character
        self.workMasteries = character.masteries_can_go_up

        mainWidget = QtWidgets.QWidget()
        mainLayout = QtWidgets.QVBoxLayout()

        self.xpLabel = QtWidgets.QLabel('Total XP:' + str(character.masteries.total_exp_spent), mainWidget)
        # self.xpLabel.setFixedWidth(self.label_size)

        sArea = QtWidgets.QScrollArea(mainWidget)
        self.frame = QtWidgets.QWidget(mainWidget)
        layout = QtWidgets.QVBoxLayout()

        layout.addLayout(self.getMasteriesGroupLayout(character, 'all_battle', MasteriesGroups.all_battle, mainWidget))
        layout.addLayout(self.getMasteriesGroupLayout(character, 'all_magic', MasteriesGroups.all_magic, mainWidget))

        self.frame.setLayout(layout)
        sArea.setWidget(self.frame)

        mainLayout.addWidget(sArea)
        mainLayout.addLayout(self.getPageBtnLayout(mainWidget), QtCore.Qt.AlignLeft)


        mainWidget.setStyleSheet('background-color: rgba(0, 0, 0, 0);color:white')
        mainWidget.setLayout(mainLayout)
        self.mainWidget = self.gamePages.gameRoot.scene.addWidget(mainWidget)
        self.gamePages.gameRoot.scene.removeItem(self.mainWidget)
        self.resized()

    def getMasteriesGroupLayout(self, character, groupName, masteries, parent):
        layout = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel(groupName, parent)
        layout.addWidget(label)
        mgLayout = QtWidgets.QHBoxLayout()
        for masteri in masteries:
            mgLayout.addLayout(self.getMasteriLayout(character, masteri, parent))
        layout.addLayout(mgLayout)
        return layout

    def getMasteriLayout(self, character, mastery, parent):
        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignCenter)
        pixmap = self.gamePages.gameRoot.cfg.getPicFile(str(mastery.name).lower() + '.png', 101003001)
        label = QtWidgets.QLabel(str(mastery.name), parent)
        label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(label)
        icon = QtWidgets.QLabel(parent)
        icon.setPixmap(pixmap)
        icon.setFixedSize(pixmap.size())
        layout.addWidget(icon)
        layout.setAlignment(icon, QtCore.Qt.AlignCenter)
        currentLevel = QtWidgets.QLabel(str(character.masteries.values[mastery]), parent)
        currentLevel.setFixedWidth(self.label_size)
        currentLevel.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(currentLevel)
        button = QtWidgets.QPushButton(str(character.masteries.calculate_cost(mastery)[0]), parent)
        button.setFixedWidth(self.label_size)
        button.setStyleSheet(self.buttonStyle)
        button.setProperty('mastery', mastery)
        button.clicked.connect(self.upClick)
        layout.setAlignment(icon, QtCore.Qt.AlignCenter)
        if mastery in self.workMasteries:
            button.setEnabled(True)
            icon.setStyleSheet('border: 1px solid blue')
        else:
            button.setEnabled(False)
        self.addToMasteriesDict(mastery, button, icon, currentLevel)
        layout.addWidget(button)
        layout.setAlignment(button, QtCore.Qt.AlignCenter)
        return layout

    def addToMasteriesDict(self, mastery, button, icon, currentLevel):
        l = self.masteriesDict.get(mastery.name)
        if l is None:
            self.masteriesDict[mastery.name] = []
            self.masteriesDict[mastery.name].append((button, icon, currentLevel))
        else:
            self.masteriesDict[mastery.name].append((button, icon, currentLevel))

    def updateMasteriesWidgets(self, mastery):
        l = self.masteriesDict.get(mastery.name)
        if not l is None:
            for item in self.masteriesDict.get(mastery.name):
                item[0].setEnabled(False)
                item[0].setText(str(self.character.temp_masteries.calculate_cost(mastery)[0]))
                item[1].setStyleSheet('border: 1px solid black')
                item[2].setText(str(self.character.temp_masteries.values[mastery]))
                self.xpLabel.setText('Total XP:' + str(self.character.temp_masteries.total_exp_spent))

    def upgradedMasteriesWidgets(self):
        self.xpLabel.setText('Total XP:' + str(self.character.masteries.total_exp_spent))
        for items in self.masteriesDict.values():
            item = items[0]
            item[0].setEnabled(True)
            mastery = item[0].property('mastery')
            item[0].setText(str(self.character.masteries.calculate_cost(mastery)[0]))
            item[1].setStyleSheet('border: 1px solid blue')
            item[2].setText(str(self.character.masteries.values[mastery]))

    def resized(self):
        self.w = self.frame.width() + 25
        if self.gamePages.gameRoot.cfg.dev_size[1] < self.frame.height():
            self.h = self.gamePages.gameRoot.cfg.dev_size[1] - 100
        else:
            self.h = self.frame.height() + 100
        if self.gamePages.gameRoot.cfg.dev_size[0] < self.frame.width() + 25:
            self.w = self.gamePages.gameRoot.cfg.dev_size[0] - 100
        else:
            self.w = self.frame.width() + 25
        x = (self.gamePages.gameRoot.cfg.dev_size[0] - self.w) / 2
        y = (self.gamePages.gameRoot.cfg.dev_size[1] - self.h) / 2
        self.mainWidget.setPos(x, y)
        self.mainWidget.widget().setFixedSize(self.w, self.h)
        self.background.setRect(x, y, self.w, self.h)
        pass

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_M:
                self.showPage()
        pass

    def showPage(self):
        if self.state:
            self.focusable.emit(False)
            self.hidePage()
        else:
            self.state = True
            self.gamePages.page = self
            self.gamePages.visiblePage = True
            self.gamePages.gameRoot.scene.addItem(self)
            self.gamePages.gameRoot.scene.addItem(self.mainWidget)
            self.upgradedMasteriesWidgets()

    def hidePage(self):
        self.state = False
        self.gamePages.page = self.gamePages.gameMenu
        self.gamePages.visiblePage = False
        self.gamePages.gameRoot.scene.removeItem(self)
        self.gamePages.gameRoot.scene.removeItem(self.mainWidget)

    def destroy(self):
        self.mainWidget.widget().destroy()
        if not self.mainWidget.scene() is None:
            self.gamePages.gameRoot.scene.removeItem(self.mainWidget)
        del self.mainWidget

    def mousePress(self, e):
        self.mousePos = e.pos()
        if self.state:
            focusState = self.mainWidget.widget().geometry().contains(e.pos().x(), e.pos().y())
            if focusState:
                self.focusable.emit(True)
            else:
                self.focusable.emit(False)
                self.hidePage()

    def upClick(self):
        widget = self.mainWidget.widget().focusWidget()
        self.gamePages.gameRoot.lengine.character.increase_mastery(widget.property('mastery'))
        self.updateMasteriesWidgets(widget.property('mastery'))

    def getPageBtnLayout(self, parent):
        btnLayout = QtWidgets.QHBoxLayout()
        btnLayout.setAlignment(QtCore.Qt.AlignLeft)
        self.ok = QtWidgets.QPushButton("ok", parent)
        self.ok.setStyleSheet(self.buttonStyle)
        self.ok.setFixedWidth(100)
        btnLayout.addWidget(self.ok)

        self.save = QtWidgets.QPushButton("save", parent)
        self.save.setStyleSheet(self.buttonStyle)
        self.save.setFixedWidth(100)
        btnLayout.addWidget(self.save)

        return btnLayout

    def okSlot(self):
        self.comitToChacracter()
        self.showPage()

    def saveSlot(self):
        self.comitToChacracter()

    def comitToChacracter(self):
        self.gamePages.gameRoot.lengine.character.commit()
        pass

    def setUpGui(self):
        self.save.clicked.connect(self.saveSlot)
        self.ok.clicked.connect(self.okSlot)

    def getLabelSize(self):
        label = QtWidgets.QLabel('1234500')
        label.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        return label.sizeHint().width()



