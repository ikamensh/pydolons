from PySide2 import QtCore, QtGui, QtWidgets


class NotifyText(QtWidgets.QGraphicsTextItem):
    def __init__(self, parent = None):
        QtWidgets.QGraphicsTextItem.__init__(self, parent)
        self.gameRoot = None
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.timerSlot)
        self.setVisible(False)

    def showText(self, text):
        self.setOpacity(1.0)
        self.setPlainText(str(text))
        x = self.gameRoot.cfg.dev_size[0] - self.boundingRect().width()
        y = self.gameRoot.cfg.dev_size[1] - self.boundingRect().height()
        x = x / 2
        y = y / 2
        self.setPos(x, y)
        self.setVisible(True)
        self.timer.start(500)

    def timerSlot(self):
        self.setOpacity(self.opacity() - 0.1)
        if self.opacity() < 0.3:
            self.setVisible(False)
            self.timer.stop()
