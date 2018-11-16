from PySide2 import QtGui, QtCore, QtWidgets

from ui.GamePages import AbstractPage

from character.masteries.MasteriesEnumSimple import MasteriesEnum, MasteriesGroups

class MasteriesPage(AbstractPage):
    """docstring for DefaultPage.
    """
    def __init__(self, gamePages):
        super().__init__(gamePages)
        self.w = 700
        self.h = 600
        self.mousePos = QtCore.QPoint(0, 0)
        self.buttonStyle = 'QPushButton{background-color:grey;color:black;}QPushButton:pressed{background-color:white;color:black;}'
        self.masteriesDict = {}
        self.setUpWidgets()
        self.workMasteries = None
        pass

    def setUpWidgets(self):
        self.background = QtWidgets.QGraphicsRectItem(0, 0, self.w, self.h)
        self.background.setBrush(QtGui.QBrush(QtCore.Qt.black))
        self.addToGroup(self.background)

        character = self.gamePages.gameRoot.lengine.character
        self.workMasteries = character.masteries_can_go_up

        mainWidget = QtWidgets.QScrollArea()
        frame = QtWidgets.QWidget(mainWidget)
        layout = QtWidgets.QVBoxLayout()
        layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)

        layout.addLayout(self.getMasteriesGroupLayout('chop_chop_chop', MasteriesGroups.chop_chop_chop, mainWidget), QtCore.Qt.AlignLeft)
        layout.addLayout(self.getMasteriesGroupLayout('stabby', MasteriesGroups.stabby, mainWidget), QtCore.Qt.AlignLeft)
        layout.addLayout(self.getMasteriesGroupLayout('bashy', MasteriesGroups.bashy, mainWidget), QtCore.Qt.AlignLeft)
        layout.addLayout(self.getMasteriesGroupLayout('sniping', MasteriesGroups.sniping, mainWidget), QtCore.Qt.AlignLeft)
        layout.addLayout(self.getMasteriesGroupLayout('spicky', MasteriesGroups.spicky, mainWidget), QtCore.Qt.AlignLeft)
        layout.addLayout(self.getMasteriesGroupLayout('loud', MasteriesGroups.loud, mainWidget), QtCore.Qt.AlignLeft)
        layout.addLayout(self.getMasteriesGroupLayout('explosive', MasteriesGroups.explosive, mainWidget), QtCore.Qt.AlignLeft)
        layout.addLayout(self.getMasteriesGroupLayout('cold', MasteriesGroups.cold, mainWidget), QtCore.Qt.AlignLeft)
        layout.addLayout(self.getMasteriesGroupLayout('arcane', MasteriesGroups.arcane, mainWidget), QtCore.Qt.AlignLeft)
        layout.addLayout(self.getMasteriesGroupLayout('chemical', MasteriesGroups.chemical, mainWidget), QtCore.Qt.AlignLeft)
        layout.addLayout(self.getMasteriesGroupLayout('all_battle', MasteriesGroups.all_battle, mainWidget), QtCore.Qt.AlignLeft)
        layout.addLayout(self.getMasteriesGroupLayout('all_magic', MasteriesGroups.all_magic, mainWidget), QtCore.Qt.AlignLeft)


        frame.setLayout(layout)
        mainWidget.setWidget(frame)

        mainWidget.setFixedSize(self.w, self.h)
        mainWidget.setStyleSheet('background-color: rgba(0, 0, 0, 0);color:white')
        self.mainWidget = self.gamePages.gameRoot.scene.addWidget(mainWidget)
        self.gamePages.gameRoot.scene.removeItem(self.mainWidget)
        self.resized()

    def getMasteriesGroupLayout(self, groupName, masteries, parent):
        layout = QtWidgets.QVBoxLayout()
        layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        label = QtWidgets.QLabel(groupName, parent)
        layout.addWidget(label)
        mgLayout = QtWidgets.QHBoxLayout()
        mgLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        for masteri in masteries:
            mgLayout.addLayout(self.getMasteriLayout(masteri, parent), QtCore.Qt.AlignLeft)
        layout.addLayout(mgLayout)
        return layout

    def getMasteriLayout(self, masteri, parent):
        layout = QtWidgets.QVBoxLayout()
        layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        pixmap = self.gamePages.gameRoot.cfg.pix_maps.get(str(masteri.name).lower() + '.png')
        if pixmap is None:
            pixmap = self.gamePages.gameRoot.cfg.pix_maps.get('default_masteri.png')
        pixmap = pixmap.scaled(32, 32)
        label = QtWidgets.QLabel(str(masteri.name), parent)
        layout.addWidget(label)
        icon = QtWidgets.QLabel(parent)
        icon.setPixmap(pixmap)
        icon.setFixedSize(pixmap.size())
        layout.addWidget(icon)
        button = QtWidgets.QPushButton('up', parent)
        button.setFixedWidth(pixmap.width())
        button.setStyleSheet(self.buttonStyle)
        button.setProperty('mastery', masteri)
        button.clicked.connect(self.upClick)
        if masteri in self.workMasteries:
            button.setEnabled(True)
            icon.setStyleSheet('border: 1px solid blue')
        else:
            button.setEnabled(False)
        self.addToMasteriesDict(masteri, button, icon)
        layout.addWidget(button)
        return layout

    def addToMasteriesDict(self, mastery, button, icon):
        l = self.masteriesDict.get(mastery.name)
        if l is None:
            self.masteriesDict[mastery.name] = []
            self.masteriesDict[mastery.name].append((button, icon))
        else:
            self.masteriesDict[mastery.name].append((button, icon))

    def updateMasteriesWidgets(self, mastery):
        l = self.masteriesDict.get(mastery.name)
        if not l is None:
            for item in self.masteriesDict.get(mastery.name):
                item[0].setEnabled(False)
                item[1].setStyleSheet('border: 1px solid black')

    def resized(self):
        x = (self.gamePages.gameRoot.cfg.dev_size[0] - self.w) / 2
        y = (self.gamePages.gameRoot.cfg.dev_size[1] - self.h) / 2
        self.mainWidget.setPos(x, y)
        self.background.setRect(x, y, self.w, self.h)
        pass

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_M:
                self.showPage()
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

    def destroy(self):
        self.mainWidget.widget().destroy()
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
        self.updateMasteriesWidgets(widget.property('mastery'))
        self.gamePages.gameRoot.lengine.character.increase_mastery(widget.property('mastery'))



