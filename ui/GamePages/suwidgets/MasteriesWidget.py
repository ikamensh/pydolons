from PySide2 import QtCore, QtWidgets

from character.masteries.MasteriesEnumSimple import MasteriesGroups


class MasteriesWidget(QtWidgets.QWidget):
    """docstring for DefaultPage.
    """
    def __init__(self, page, parent = None):
        super().__init__(parent = None)
        self.gamePages = page.gamePages
        self.character = page.gamePages.gameRoot.lengine.character
        self.buttonStyle = 'QPushButton{background-color:grey;color:black;}QPushButton:pressed{background-color:white;color:black;}'
        self.masteriesDict = {}
        self.label_size = self.getLabelSize()
        self.setUpWidgets()
        self.workMasteries = None
        pass

    def setUpWidgets(self):
        self.workMasteries = self.character.masteries_can_go_up


        self.xpLabel = QtWidgets.QLabel('Total XP:' + str(self.character.masteries.total_exp_spent), self)
        # self.xpLabel.setFixedWidth(self.label_size)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.xpLabel)
        layout.addLayout(self.getMasteriesGroupLayout(self.character, 'all_battle', MasteriesGroups.all_battle, self))
        layout.addLayout(self.getMasteriesGroupLayout(self.character, 'all_magic', MasteriesGroups.all_magic, self))
        self.setLayout(layout)


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
        self.masteriesDict[mastery] = (button, icon, currentLevel)

    def updateMasteriesWidgets(self, mastery):
        l = self.masteriesDict.get(mastery.name)
        if not l is None:
            for item in self.masteriesDict.get(mastery.name):
                item[0].setEnabled(False)
                item[0].setText(str(self.character.temp_masteries.calculate_cost(mastery)[0]))
                item[1].setStyleSheet('border: 1px solid black')
                item[2].setText(str(self.character.temp_masteries.values[mastery]))
                self.xpLabel.setText('Total XP:' + str(self.character.temp_masteries.total_exp_spent))

    def updatePage(self):
        self.xpLabel.setText('Total XP:' + str(self.character.masteries.total_exp_spent))
        for item in self.masteriesDict.values():
            item[0].setEnabled(True)
            mastery = item[0].property('mastery')
            item[0].setText(str(self.character.masteries.calculate_cost(mastery)[0]))
            item[1].setStyleSheet('border: 1px solid blue')
            item[2].setText(str(self.character.masteries.values[mastery]))

    def upClick(self):
        widget = self.focusWidget()
        self.character.increase_mastery(widget.property('mastery'))
        self.updatePage()

    def getLabelSize(self):
        label = QtWidgets.QLabel('1234500')
        label.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        return label.sizeHint().width()




