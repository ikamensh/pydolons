from PySide2.QtCore import Qt, QPropertyAnimation
from PySide2.QtGui import QFont
from PySide2.QtWidgets import QGraphicsTextItem


class HealthText(QGraphicsTextItem):
    def __init__(self):
        super(HealthText, self).__init__()
        self.w = 128
        self.h = 128
        self.start_y = 0
        self.setFont(QFont("Times", 36, 10, False))
        self.setVisible(False)
        self.anim_move = QPropertyAnimation(self, b'y')
        self.anim_move.setDuration(600)
        self.anim_move.setStartValue(self.start_y)
        self.anim_move.setEndValue(self.start_y - self.h / 2)
        self.anim_opacity = QPropertyAnimation(self, b'opacity')
        self.anim_opacity.setDuration(600)
        self.anim_opacity.setStartValue(1.0)
        self.anim_opacity.setEndValue(0.0)

    def setStartY(self, y):
        if self.start_y == 0:
            self.start_y = y

    def setText(self, value):
        self.setOpacity(1.0)
        if value < 0:
            self.setDefaultTextColor(Qt.red)
        else:
            self.setDefaultTextColor(Qt.green)
        self.setPlainText(str(value))
        self.anim_move.start()
        self.anim_opacity.start()
        self.setVisible(True)

    def setUnitPos(self, pos):
        self.setPos(pos.x() + 32, pos.y() - 64)

    def setOffset(self, x, y):
        # self.setPos(x + 32, y - 32)
        pass
