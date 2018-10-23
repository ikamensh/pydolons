from PySide2 import QtCore,  QtWidgets

class Actives(QtCore.QObject):
    setTargets = QtCore.Signal(list)
    def __init__(self, page, parent = None, widget_size = (64, 64), margin = 10, columns = 3):
        super(Actives, self).__init__(parent)
        self.page = page
        self.hero = None
        self.names = None
        self.mWidget = None
        self.scrollArea = None
        self.widget_size = widget_size
        self.toolTip= None
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
        self.setUp()
        self.addActiveButtons()

    def setActivesSize(self):
        self.w = self.frame_size[0] + 16
        self.h = self.widget_size[1] + 2 * self.margin
        if not self.scrollArea is None:
            step = self.h - int(self.margin / 2)
            self.scrollArea.verticalScrollBar().setSingleStep(step)
            self.scrollArea.setMinimumSize(self.w, self.h)
            self.scrollArea.setFixedSize(self.w, self.h)

    def setFrameSize(self, size:set, col:int, row:int):
        w = size[0] * col + self.margin * (col + 2)
        h = size[1] * row + self.margin * (row + 2)
        self.frame_size = (w, h)
        if not self.mWidget is None:
            self.mWidget.setMinimumSize(self.frame_size[0], self.frame_size[1])



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
        # widget.ajGeometry = QtCore.QRect(self.x + widget.x, self.y + widget.y, self.widget_size[0], self.widget_size[1])
        self.widgets[name] = widget

    def addActiveButtons(self):
        self.hero = self.page.gameRoot.game.the_hero
        for active in self.hero.actives:
            self.addWidget(active.name)
            widget = self.widgets[active.name]
            widget.pressed.connect(self.selectActive)
            widget.setProperty('status', active.owner_can_afford_activation())
            widget.setProperty('active', active)
            widget.setStyleSheet('QPushButton[status = "true"]{' \
                                         'background-color:green;}' \
                                         'QPushButton[status = "false"]{' \
                                         'background-color:gray;}' \
                                         'QPushButton:pressed {' \
                                         'background-color: white;' \
                                         'color:black}')


    def setNames(self):
        self.names = ['run',
                      'back',
                      'atack',
                      'block',
                      'hide']
        for i in range(6, 25, 1):
            self.names.append('active_' + str(i))

    def setUp(self):
        margin = QtCore.QMargins(0, 0, 0, 0)
        self.layout = QtWidgets.QGridLayout()
        self.layout.setContentsMargins(margin)
        self.layout.setMargin(0)
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setStyleSheet('background-color:black;' \
                                      'color:white;')
        self.scrollArea.setMinimumSize(self.w, self.h)
        self.scrollArea.setFixedSize(self.w, self.h)
        self.scrollArea.setSizePolicy(self.sizePolicy)
        self.mWidget = QtWidgets.QWidget()
        self.mWidget.setMinimumSize(self.frame_size[0], self.frame_size[1])
        self.mWidget.setLayout(self.layout)
        self.scrollArea.setWidget(self.mWidget)
        self.toolTip = QtWidgets.QLabel()
        self.toolTip.setFixedSize(128, 64)
        self.toolTip.setVisible(False)
        self.toolTip.setStyleSheet('background-color:black;'\
                                   'color:white;')

    def updatePos(self, size):
        self.x = size[0] / 2 - self.w /2
        self.y = size[1] - self.h - 5
        self.scrollArea.move(self.x , self.y )
        if self.widgets!= {}:
            print('ad dfsf')
            for widget in self.widgets.values():
                widget.ajGeometry = QtCore.QRect(self.x + widget.x(), self.y + widget.y(), self.widget_size[0], self.widget_size[1])

    def selectActive(self):
        active = self.mWidget.focusWidget().property('active')
        targets = self.page.gameRoot.game.get_possible_targets(active)
        if not targets is None:
            if targets:
                self.setTargets.emit(targets)
        else:
            print(None)

    def showToolTip(self, widget, pos):
        self.toolTip.move(pos.x(), pos.y() - 64)
        self.toolTip.setText(widget.text())
        self.toolTip.setVisible(True)

    def setScene(self, scene):
        self.prxScrollArea = scene.addWidget(self.scrollArea)
        self.prxToolTip = scene.addWidget(self.toolTip)
        self.prxToolTip.setOpacity(0.8)



    def collisioon(self, pos):
        for widget in self.widgets.values():
            qr = QtCore.QRect(self.x + self.mWidget.x() + widget.x(), self.y + self.mWidget.y() + widget.y(), self.widget_size[0], self.widget_size[1])
            if qr.contains(pos.x(), pos.y()):
                self.showToolTip(widget, pos)
                break
            else:
                self.toolTip.setVisible(False)