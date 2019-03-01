from PySide2 import QtGui, QtCore, QtWidgets

from ui.GamePages import AbstractPage


class SettingsPage(AbstractPage):
    """docstring for StartPage."""
    def __init__(self, gamePages):
        super().__init__(gamePages)
        self.w = 320
        self.h = 240
        self.isService = True
        self.setUpWidgets()
        self.gamePages.gameRoot.view.wheel_change.connect(self.updatePos)

    def setUpWidgets(self):
        self.background = QtWidgets.QGraphicsPixmapItem(self.gamePages.gameRoot.cfg.getPicFile('arena.jpg'))
        self.resizeBackground(self.background)
        self.addToGroup(self.background)

        mainWidget = QtWidgets.QWidget()
        mainWidget.resize(self.w, self.h)
        # mainWidget.setStyleSheet('background-color: rgba(0, 0, 0, 0);')

        formlayout = QtWidgets.QFormLayout(mainWidget)

        formlayout.addRow('Device\nresolution', QtWidgets.QLabel(self.res_to_str(self.gamePages.gameRoot.cfg.deviceConfig.device_resolution)))

        self.resolution = self.getResolutions()
        formlayout.addRow('Resolutions', self.resolution)

        self.select_resolution = QtWidgets.QLabel('', parent=mainWidget)
        self.select_resolution.setText(self.res_to_str(self.resolution.itemData(self.resolution.currentIndex())))

        formlayout.addRow('Select\nresolution', self.select_resolution)

        self.fullscreen = self.getCheckBox(mainWidget, 'Full screen', formlayout, self.ceckFullScreenBox)
        save = QtWidgets.QPushButton('SAVE')
        save.clicked.connect(self.saveSlot)
        formlayout.addRow('save\nchanges', save)

        mainWidget.setLayout(formlayout)
        self.readFromConfig()
        self.mainWidget = self.gamePages.gameRoot.scene.addWidget(mainWidget)
        self.mainWidget.setFlags(QtWidgets.QGraphicsItem.ItemIgnoresTransformations)
        self.gamePages.gameRoot.scene.removeItem(self.mainWidget)
        self.resized()

        # brush = QtGui.QBrush(self.gamePages.gameRoot.cfg.getPicFile('scroll_background.png'))

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

    def getDeviceResolution(self):
        return QtWidgets.QLabel(self.dev_resolution)

    def getResolutions(self):
        resolution = QtWidgets.QComboBox()
        resolution.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLengthWithIcon)
        resolution.activated.connect(self.changeResolution)
        for res in self.gamePages.gameRoot.cfg.resolutions:
            resolution.addItem(str(res[0])+'x'+str(res[1]), res)

        return resolution

    def changeResolution(self, index):
        self.gamePages.gameRoot.cfg.userConfig.setSize(self.resolution.itemData(index))
        self.select_resolution.setText(self.res_to_str(self.resolution.itemData(index)))

    def getCheckBox(self, mainWidget, name = None, formLayout = None, slot = None):
        checkBox = QtWidgets.QCheckBox(parent=mainWidget)
        if formLayout is not None:
            if name is None:
                formLayout.addRow('check_box', checkBox)
            else:
                formLayout.addRow(name, checkBox)
        if slot is not None:
            checkBox.clicked.connect(slot)
        return checkBox

    def ceckFullScreenBox(self):
        if self.fullscreen.isChecked():
            self.resolution.setEnabled(False)
            self.gamePages.gameRoot.cfg.userConfig.read_config['window']['fullscreen'] = True
            index = self.gamePages.gameRoot.cfg.resolutions.index(self.gamePages.gameRoot.cfg.deviceConfig.device_resolution)
            self.resolution.setCurrentIndex(index)
            self.select_resolution.setText(self.res_to_str(self.gamePages.gameRoot.cfg.deviceConfig.device_resolution))
            self.gamePages.gameRoot.cfg.userConfig.setSize(self.gamePages.gameRoot.cfg.deviceConfig.device_resolution)
        else:
            self.gamePages.gameRoot.cfg.userConfig.read_config['window']['fullscreen'] = False
            self.resolution.setEnabled(True)

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            if self.state:
                self.hidePage()

    def updatePos(self):
        super().updatePos()
        self.mainWidget.setPos(self.gamePages.gameRoot.view.mapToScene(self.widget_pos))

    def resized(self):
        super().resized()
        self.widget_pos.setX((self.gamePages.gameRoot.cfg.dev_size[0] - self.w) / 2)
        self.widget_pos.setY((self.gamePages.gameRoot.cfg.dev_size[1] - self.h) / 2)
        self.mainWidget.setPos(self.widget_pos)
        self.resizeBackground(self.background)
        pass

    @property
    def dev_resolution(self):
        return str(self.gamePages.gameRoot.cfg.dev_size[0])+'x'+str(self.gamePages.gameRoot.cfg.dev_size[1])

    def res_to_str(self, size):
        return str(size[0])+'x'+str(size[1])

    def saveSlot(self):
        try:
            self.gamePages.gameRoot.cfg.userConfig.saveSetting()
        except Exception as e:
            print('D\'ont save conifg!')

    def readFromConfig(self):
        if self.gamePages.gameRoot.cfg.userConfig.read_config['window']['fullscreen']:
            self.fullscreen.setChecked(True)
            self.resolution.setEnabled(False)
        else:
            w = self.gamePages.gameRoot.cfg.userConfig.read_config['window']['resolution']['width']
            h = self.gamePages.gameRoot.cfg.userConfig.read_config['window']['resolution']['height']
            index = self.gamePages.gameRoot.cfg.resolutions.index((w, h))
            self.resolution.setCurrentIndex(index)
            self.select_resolution.setText(str(w)+'x'+str(h))


