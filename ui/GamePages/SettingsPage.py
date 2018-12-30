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

        formlayout.addRow('Device\nresolution', QtWidgets.QLabel(self.dev_resolution))

        self.resolution = self.getResolutions()
        formlayout.addRow('Resolutions', self.resolution)

        self.select_resolution = QtWidgets.QLabel(self.dev_resolution)
        formlayout.addRow('Select\nresolution', self.select_resolution)

        self.fullscreen = self.getFullScreen()
        formlayout.addRow('Fullscreen', self.fullscreen)

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
        resolution.addItem('current', (self.gamePages.gameRoot.cfg.dev_size[0],
                                      self.gamePages.gameRoot.cfg.dev_size[1]))
        for res in self.gamePages.gameRoot.cfg.resolutions:
            resolution.addItem(str(res[0])+'x'+str(res[1]), res)
        return resolution

    def changeResolution(self, index):
        size = self.resolution.itemData(index)
        self.gamePages.gameRoot.cfg.user_cfg.read_config['window']['resolution'] = {'width': size[0], 'height': size[1]}
        self.gamePages.gameRoot.cfg.user_cfg.read_config['window']['fullscreen'] = False
        self.gamePages.gameRoot.view.changeResolution(size[0], size[1])
        self.gamePages.gameRoot.ui.setMinimumSize(self.resolution.itemData(index)[0], self.resolution.itemData(index)[1])

        self.select_resolution.setText(self.dev_resolution)
        self.gamePages.gameRoot.ui.showNormal()

    def getFullScreen(self):
        fullscreen = QtWidgets.QCheckBox()
        fullscreen.clicked.connect(self.changeFullScreen)
        return fullscreen

    def changeFullScreen(self):
        if self.fullscreen.isChecked():
            self.resolution.setEnabled(False)
            self.gamePages.gameRoot.cfg.user_cfg.read_config['window']['fullscreen'] = True
            self.gamePages.gameRoot.ui.showFullScreen()
            self.gamePages.gameRoot.view.resized.emit()
        else:
            self.resolution.setEnabled(True)
            self.gamePages.gameRoot.ui.showNormal()

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
        if self.fullscreen.isChecked():
            self.select_resolution.setText(self.dev_resolution)
        pass

    @property
    def dev_resolution(self):
        return str(self.gamePages.gameRoot.cfg.dev_size[0])+'x'+str(self.gamePages.gameRoot.cfg.dev_size[1])

    def saveSlot(self):
        if self.fullscreen.isChecked():
            self.gamePages.gameRoot.cfg.user_cfg.read_config['window']['resolution'] = 'current'
            self.gamePages.gameRoot.cfg.user_cfg.read_config['window']['fullscreen'] = True
        else:
            if self.gamePages.gameRoot.cfg.dev_size not in self.gamePages.gameRoot.cfg.resolutions:
                w, h = self.gamePages.gameRoot.cfg.device_resolution
            else:
                w, h = self.gamePages.gameRoot.cfg.dev_size
            self.gamePages.gameRoot.cfg.user_cfg.read_config['window']['resolution'] = {'width':w, 'height':h}
            self.gamePages.gameRoot.cfg.user_cfg.read_config['window']['fullscreen'] = False
        try:
            self.gamePages.gameRoot.cfg.user_cfg.saveSetting()
        except Exception as e:
            print('D\'ont save conifg!')

    def readFromConfig(self):
        if self.gamePages.gameRoot.cfg.user_cfg.read_config['window']['fullscreen']:
            self.fullscreen.setCheckState(QtCore.Qt.Checked)
            self.resolution.setEnabled(False)
        else:
            w = self.gamePages.gameRoot.cfg.user_cfg.read_config['window']['resolution']['width']
            h = self.gamePages.gameRoot.cfg.user_cfg.read_config['window']['resolution']['height']
            index = self.gamePages.gameRoot.cfg.resolutions.index((w, h))
            self.resolution.setCurrentIndex(index+1)
            self.select_resolution.setText(str(w)+'x'+str(h))

