from PySide2 import QtWidgets, QtCore


class GuiConsole(QtWidgets.QPlainTextEdit):
    def __init__(self, log, *args):
        super(GuiConsole, self).__init__(*args)
        self.last_msg = None
        self.setStyleSheet('background-color:black; color: green;')
        self.log = log
        self.state = True
        self.mousePos = QtCore.QPoint(0, 0)
        self.widget_pos = QtCore.QPoint()
        self.rect = QtCore.QRectF()
        self.addWidgets()

    def addWidgets(self):
        self.btn = QtWidgets.QPushButton('>', self)
        self.btn.setFixedSize(20, 20)
        buttonStyle = 'QPushButton{background-color:black;color:white;}QPushButton:pressed{background-color:white;color:black;}'
        self.btn.setStyleSheet(buttonStyle)
        self.btn.clicked.connect(self.pressBtn)

    def pressBtn(self):
        if self.state:
            x = self.widget_pos.x() - self.btn.width() + self.width()
            self.state = False
        else:
            x = self.widget_pos.x() + self.btn.width() - self.width()
            self.state = True
        self.widget_pos.setX(x)
        self.rect.setRect(
            self.widget_pos.x(),
            self.widget_pos.y(),
            self.width(),
            self.height())

    def timerEvent(self, e):
        if self.last_msg != self.log.msg:
            self.last_msg = self.log.msg
            self.appendPlainText(str(self.last_msg))

    def resized(self, dev_size):
        if self.state:
            self.widget_pos.setX(dev_size[0] - self.width())
        else:
            self.widget_pos.setX(dev_size[0] - self.btn.width())
        self.widget_pos.setY(dev_size[1] - self.height())
        self.rect.setRect(
            self.widget_pos.x(),
            self.widget_pos.y(),
            self.width(),
            self.height())

    def setMousePos(self, e):
        self.mousePos = e.pos()

    def isFocus(self):
        return self.rect.contains(self.mousePos)
