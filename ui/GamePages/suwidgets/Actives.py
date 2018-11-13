from PySide2 import QtCore, QtWidgets

class Actives(QtCore.QObject):
    setTargets = QtCore.Signal(list)
    def __init__(self, page, parent = None, widget_size = (64, 64), margin = 10, columns = 3):
        super(Actives, self).__init__(parent)
        self.x, self.y = 0, 0
        self.rect = QtCore.QRectF(self.x, self.y, 1, 1)
        self.mousePos = QtCore.QPoint(0, 0)
        self.page = page
        self.hero = None
        self.names = None
        self.frame = None
        self.widget_size = widget_size
        self.widgets = {}
        self.margin = margin
        self.n = 1
        self.columns = columns
        self.rows = 1

        self.row = 0
        self.column = 0

        self.sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.setFrameSize(self.widget_size, 1, 1)
        self.setActivesSize()
        self.setNames()
        self.setUpWidgets()
        self.addActiveButtons()

    def setActivesSize(self):
        self.w = self.frame_size[0] + 16
        self.h = self.widget_size[1] + 2 * self.margin
        self.rect.setWidth(self.w)
        self.rect.setHeight(self.h)


    def setFrameSize(self, size:set, col:int, row:int):
        w = size[0] * col + self.margin * (col + 2)
        h = size[1] * row + self.margin * (row + 2)
        self.frame_size = (w, h)
        if not self.frame is None:
            self.frame.setMinimumSize(self.frame_size[0], self.frame_size[1])



    def addWidget(self, name):
        widget = QtWidgets.QPushButton(name)
        widget.setMinimumSize(self.widget_size[0], self.widget_size[1])
        widget.setFixedSize(self.widget_size[0], self.widget_size[1])
        widget.setSizePolicy(self.sizePolicy)
        self.layout.addWidget(widget, self.row, self.column)
        if self.n % self.columns == 0:
            self.row = self.rows
            self.rows += 1
            self.column = 0
        else:
            self.column += 1
        self.n += 1
        self.setFrameSize(self.widget_size,  self.columns, self.rows)
        self.setActivesSize()
        widget.ajGeometry = QtCore.QRect(self.x + widget.x(), self.y + widget.y(), self.widget_size[0], self.widget_size[1])
        self.widgets[name] = widget

    def addActiveButtons(self):
        self.hero = self.page.gamePages.gameRoot.game.the_hero
        for active in self.hero.actives:
            self.addWidget(active.name)
            widget = self.widgets[active.name]
            widget.pressed.connect(self.selectActive)
            widget.setProperty('status', active.owner_can_afford_activation())
            widget.setProperty('active', active)
            widget.setStyleSheet('QPushButton[status = "true"]{'
                             'background-color:green;}'
                             'QPushButton[status = "false"]{'
                             'background-color:gray;}'
                             'QPushButton:pressed {'
                             'background-color: white;'
                             'color:black}')


    def setNames(self):
        self.names = ['run',
                      'back',
                      'atack',
                      'block',
                      'hide']
        for i in range(6, 25, 1):
            self.names.append('active_' + str(i))

    def setUpWidgets(self):
        margin = QtCore.QMargins(0, 0, 0, 0)

        self.mainWidget = QtWidgets.QWidget()
        self.mainWidget.setStyleSheet('background-color: black;color:white')
        mainLayout = QtWidgets.QHBoxLayout()
        mainLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        mainLayout.setAlignment(QtCore.Qt.AlignRight)
        mainLayout.setMargin(0)

        btnLayout = QtWidgets.QVBoxLayout()
        btnLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        btnLayout.setAlignment(QtCore.Qt.AlignRight)
        btnLayout.setMargin(0)
        btnLayout.setContentsMargins(margin)

        buttonStyle = 'QPushButton{background-color:black;color:white;}QPushButton:pressed{background-color:white;color:black;}'

        self.up = QtWidgets.QPushButton('^', self.mainWidget)
        self.up.setFixedSize(40, 30)
        self.up.setStyleSheet(buttonStyle)
        btnLayout.addWidget(self.up, QtCore.Qt.AlignRight)

        self.down = QtWidgets.QPushButton('V', self.mainWidget)
        self.down.setFixedSize(40, 30)
        self.down.setStyleSheet(buttonStyle)
        btnLayout.addWidget(self.down, QtCore.Qt.AlignRight)

        self.layout = QtWidgets.QGridLayout()
        self.layout.setContentsMargins(margin)
        self.layout.setMargin(0)
        self.frame = QtWidgets.QWidget(self.mainWidget)
        self.frame.setMinimumSize(self.frame_size[0], self.frame_size[1])
        self.frame.setLayout(self.layout)
        mainLayout.addLayout(btnLayout)
        self.mainWidget.setLayout(mainLayout)
        self.up.pressed.connect(self.upSlot)
        self.down.pressed.connect(self.downSlot)
        self.mainWidget:QtWidgets.QGraphicsProxyWidget = self.page.gamePages.gameRoot.scene.addWidget(self.mainWidget)
        self.resized()


    def resized(self, size = None):
        size = self.page.gamePages.gameRoot.cfg.dev_size
        self.x = size[0] / 2 - self.w /2
        self.y = size[1] - self.h
        self.mainWidget.setPos(self.x, self.y)
        self.mainWidget.widget().setFixedSize(self.w + 30, self.h)
        self.rect.moveTo(self.x, self.y)

    def selectActive(self):
        active = self.frame.focusWidget().property('active')
        targets = self.page.gamePages.gameRoot.game.get_possible_targets(active)
        if not targets is None:
            if targets:
                self.setTargets.emit(targets)

    def showPrxToolTip(self, widget, pos):
        self.prxToolTip.setPos(pos.x(), pos.y() - 64)
        self.prxToolTip.widget().setText(widget.text())
        self.prxToolTip.setVisible(True)


    def mouseMoveEvent(self, e):
        self.mousePos = e.pos()
        if self.mainWidget.geometry().contains(e.pos()):
            self.collision(e.pos())

    def collision(self, pos):
        for widget in self.widgets.values():
            qr = QtCore.QRect(self.x + self.frame.x() + widget.x(), self.y + self.frame.y() + widget.y(), self.widget_size[0], self.widget_size[1])
            if qr.contains(pos.x(), pos.y()):
                widget.setFocus()
                self.page.showToolTip(widget.text(), pos.x() + 20, pos.y() - 20)
                break
            else:
                self.page.hideToolTip()

    def destroy(self):
        del self.up
        del self.down
        del self.frame
        self.page.gamePages.gameRoot.scene.removeItem(self.mainWidget)
        del self.mainWidget

    def upSlot(self):
        print('pressed up')
        self.frame.move(0, 0)


    def downSlot(self):
        print('pressed down')
        self.frame.move(0, - self.mainWidget.widget().height())

    def isFocus(self):
        focus = self.mainWidget.widget().geometry().contains(self.mousePos.x(), self.mousePos.y())
        return focus


