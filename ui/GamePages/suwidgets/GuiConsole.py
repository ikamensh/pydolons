from PySide2 import QtWidgets
from GameLog import gamelog



class GuiConsole(QtWidgets.QPlainTextEdit):
    def __init__(self, *args):
        super(GuiConsole, self).__init__(*args)
        self.last_msg = None
        self.setStyleSheet('color: green;')

    def timerEvent(self, e):
        if self.last_msg != gamelog.msg:
            self.last_msg = gamelog.msg
            self.appendPlainText(str(self.last_msg))
