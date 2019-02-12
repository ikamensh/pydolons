from PySide2.QtCore import QTimer, Qt
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QGraphicsTextItem


class HealthText(QGraphicsTextItem):
    def __init__(self):
        super(HealthText, self).__init__()
        self.w = 128
        self.h = 128
        # self.setOpacity(1.0)
        self.setFont(QFont("Times", 36, 10, False))
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timerSlot)
        self.setVisible(False)

    def setText(self, value):
        self.setOpacity(1.0)
        if value < 0:
            self.setDefaultTextColor(Qt.red)
        else:
            self.setDefaultTextColor(Qt.green)
        self.setPlainText(str(value))
        self.setVisible(True)
        self.timer.start(500)

    def setUnitPos(self, pos):
        self.setPos(pos.x() + 32, pos.y()-64)

    def timerSlot(self):
        self.setOpacity(self.opacity() - 0.1)
        if self.opacity() < 0.3:
            self.setVisible(False)
            self.timer.stop()

    def setOffset(self, x, y):
        # self.setPos(x + 32, y - 32)
        pass
