from PySide2 import QtGui, QtWidgets, QtCore

class HealthText(QtWidgets.QGraphicsTextItem):
    def __init__(self):
        super(HealthText, self).__init__()
        self.w = 128
        self.h = 128
        # self.setOpacity(1.0)
        self.setFont(QtGui.QFont("Times", 24, 10, False))
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.timerSlot)
        self.setVisible(False)

    def setText(self, value):
        self.setOpacity(1.0)
        if value < 0:
            self.setDefaultTextColor(QtCore.Qt.red)
        else:
            self.setDefaultTextColor(QtCore.Qt.green)
        self.setPlainText(str(value))
        self.setVisible(True)
        self.timer.start(500)

    def setUnitPos(self, pos):
        self.setPos(pos.x() + 32, pos.y() - 32)

    def timerSlot(self):
        self.setOpacity(self.opacity() - 0.1)
        if self.opacity() < 0.3:
            self.setVisible(False)
            self.timer.stop()
