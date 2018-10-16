from PySide2 import QtWidgets



class GuiConsole(QtWidgets.QPlainTextEdit):
    def __init__(self, log, *args):
        super(GuiConsole, self).__init__(*args)
        self.last_msg = None
        self.setStyleSheet('color: green;')
        self.log = log

    def timerEvent(self, e):
        if self.last_msg != self.log.msg:
            self.last_msg = self.log.msg
            self.appendPlainText(str(self.last_msg))
