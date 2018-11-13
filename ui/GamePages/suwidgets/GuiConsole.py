from PySide2 import QtWidgets, QtCore



class GuiConsole(QtWidgets.QPlainTextEdit):
    def __init__(self, log, *args):
        super(GuiConsole, self).__init__(*args)
        self.last_msg = None
        self.setStyleSheet('background-color:black; color: green;')
        self.log = log
        self.state = True
        self.mousePos = QtCore.QPoint(0, 0)
        self.addWidgets()

    def addWidgets(self):
        self.btn = QtWidgets.QPushButton('>', self)
        self.btn.setFixedSize(20, 20)
        buttonStyle = 'QPushButton{background-color:black;color:white;}QPushButton:pressed{background-color:white;color:black;}'
        self.btn.setStyleSheet(buttonStyle)
        self.btn.pressed.connect(self.pressBtn)

    def pressBtn(self):
        if self.state:
            x = self.x() - self.btn.width() + self.width()
            self.move(x, self.y())
            self.state = False
        else:
            x = self.x() + self.btn.width() - self.width()
            self.move(x, self.y())
            self.state = True

    def timerEvent(self, e):
        if self.last_msg != self.log.msg:
            self.last_msg = self.log.msg
            self.appendPlainText(str(self.last_msg))

    def resized(self, dev_size):
        if self.state:
            x = dev_size[0] - self.width()
            y = dev_size[1] - self.height()
        else:
            x = dev_size[0] - self.btn.width()
            y = dev_size[1] - self.height()
        self.move(x, y)

    def setMousePos(self, e):
        self.mousePos = e.pos()

    def isFocus(self):
        return self.geometry().contains(self.mousePos)

