from PySide2.QtWidgets import QGraphicsRectItem
from PySide2.QtCore import Qt
from PySide2.QtGui import QColor


class HealthBar(QGraphicsRectItem):
    """docstring for HealtBar."""
    orange = QColor(255, 102, 0)

    def __init__(self):
        super(HealthBar, self).__init__()
        self.setBrush(Qt.red)
        self.setOpacity(0.6)

    def setColor(self, unit):
        if unit.is_obstacle:
            self.setBrush(self.orange)
        elif unit.is_hero:
            self.setBrush(Qt.cyan)

    def setHP(self, hp):
        """ По указанным процентам устанавливает длину HealtBar
        делим на 7 частей
        1/7 -- высоты героя
        6/7 -- начало отсчета
        """

        w = int(128 * hp / 100)
        h = 128 / 7
        y = (6 * 128) / 7
        self.rect().setWidth(w)
        self.setRect(0, y, w, h)

    def setOffset(self, x, y):
        # self.setPos(x + 32, y - 32)
        self.setX(x)
        self.setY(x)
        pass
